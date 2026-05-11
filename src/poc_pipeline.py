from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "Dataset"
OUTPUT_DIR = ROOT / "outputs" / "poc"
RAW_FRAMES_DIR = OUTPUT_DIR / "frames" / "raw"
ENHANCED_DIR = OUTPUT_DIR / "frames" / "enhanced"
GRID_DIR = OUTPUT_DIR / "grids"
REPORTS_DIR = OUTPUT_DIR / "reports"
CSV_PATH = OUTPUT_DIR / "frame_index.csv"
SUMMARY_PATH = REPORTS_DIR / "summary.json"
SEED = 42


torch.manual_seed(SEED)
np.random.seed(SEED)


@dataclass(frozen=True)
class PipelineSpec:
    name: str
    fn: Callable[[np.ndarray], np.ndarray]


class TinyCNN(nn.Module):
    def __init__(self, num_classes: int) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Linear(64, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)


def ensure_dirs() -> None:
    for path in [RAW_FRAMES_DIR, ENHANCED_DIR, GRID_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def iter_videos() -> list[Path]:
    return sorted(DATASET_DIR.glob("*.mp4"))


def extract_frames(sample_seconds: float = 1.0, max_frames_per_video: int = 30) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for video_path in iter_videos():
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        total_seconds = frame_count / fps if fps > 0 else 0
        step = max(int(round(fps * sample_seconds)), 1) if fps > 0 else 1
        video_id = video_path.stem
        video_dir = RAW_FRAMES_DIR / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        saved = 0
        frame_idx = 0
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            if frame_idx % step == 0:
                frame_name = f"{video_id}_f{frame_idx:05d}.jpg"
                frame_path = video_dir / frame_name
                cv2.imwrite(str(frame_path), frame)
                rows.append(
                    {
                        "video_id": video_id,
                        "video_file": str(video_path.relative_to(ROOT)),
                        "frame_idx": frame_idx,
                        "timestamp_sec": frame_idx / fps if fps > 0 else None,
                        "frame_file": str(frame_path.relative_to(ROOT)),
                        "fps": fps,
                        "frame_count": frame_count,
                        "duration_sec": total_seconds,
                    }
                )
                saved += 1
                if saved >= max_frames_per_video:
                    break
            frame_idx += 1
        cap.release()
    df = pd.DataFrame(rows).sort_values(["video_id", "frame_idx"]).reset_index(drop=True)
    df.to_csv(CSV_PATH, index=False)
    return df


def white_balance_gray_world(image_rgb: np.ndarray) -> np.ndarray:
    img = image_rgb.astype(np.float32)
    channel_means = img.reshape(-1, 3).mean(axis=0)
    overall_mean = channel_means.mean()
    gains = overall_mean / np.clip(channel_means, 1e-6, None)
    balanced = img * gains
    return np.clip(balanced, 0, 255).astype(np.uint8)


def gamma_correction(image_rgb: np.ndarray, gamma: float = 0.9) -> np.ndarray:
    inv_gamma = 1.0 / max(gamma, 1e-6)
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image_rgb, table)


def clahe_luminance(image_rgb: np.ndarray, clip_limit: float = 2.0, grid_size: int = 8) -> np.ndarray:
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
    l2 = clahe.apply(l)
    merged = cv2.merge([l2, a, b])
    return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)


def denoise_and_sharpen(image_rgb: np.ndarray) -> np.ndarray:
    denoised = cv2.bilateralFilter(image_rgb, d=5, sigmaColor=40, sigmaSpace=40)
    blurred = cv2.GaussianBlur(denoised, (0, 0), 1.0)
    sharpened = cv2.addWeighted(denoised, 1.25, blurred, -0.25, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def pipeline_clahe(image_rgb: np.ndarray) -> np.ndarray:
    return clahe_luminance(image_rgb)


def pipeline_balanced(image_rgb: np.ndarray) -> np.ndarray:
    return clahe_luminance(gamma_correction(white_balance_gray_world(image_rgb), gamma=0.95))


def pipeline_full(image_rgb: np.ndarray) -> np.ndarray:
    return denoise_and_sharpen(
        clahe_luminance(
            gamma_correction(
                white_balance_gray_world(image_rgb),
                gamma=0.9,
            )
        )
    )


PIPELINES = [
    PipelineSpec("clahe", pipeline_clahe),
    PipelineSpec("balanced", pipeline_balanced),
    PipelineSpec("full", pipeline_full),
]


def run_pipelines(frame_index: pd.DataFrame) -> pd.DataFrame:
    records = []
    for pipeline in PIPELINES:
        for _, row in frame_index.iterrows():
            src = ROOT / row["frame_file"]
            image_bgr = cv2.imread(str(src))
            if image_bgr is None:
                continue
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            enhanced = pipeline.fn(image_rgb)
            out_dir = ENHANCED_DIR / pipeline.name / row["video_id"]
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / src.name
            cv2.imwrite(str(out_path), cv2.cvtColor(enhanced, cv2.COLOR_RGB2BGR))
            records.append(
                {
                    "video_id": row["video_id"],
                    "frame_idx": row["frame_idx"],
                    "pipeline": pipeline.name,
                    "enhanced_file": str(out_path.relative_to(ROOT)),
                }
            )
    return pd.DataFrame(records)


def build_before_after_grids(frame_index: pd.DataFrame, max_examples: int = 6) -> list[str]:
    outputs: list[str] = []
    sample_df = frame_index.groupby("video_id", as_index=False).first().head(max_examples)
    for _, row in sample_df.iterrows():
        fig, axes = plt.subplots(1, 1 + len(PIPELINES), figsize=(16, 4))
        raw_rgb = cv2.cvtColor(cv2.imread(str(ROOT / row["frame_file"])), cv2.COLOR_BGR2RGB)
        axes[0].imshow(raw_rgb)
        axes[0].set_title("raw")
        axes[0].axis("off")
        for i, pipeline in enumerate(PIPELINES, start=1):
            p = ENHANCED_DIR / pipeline.name / row["video_id"] / Path(row["frame_file"]).name
            img = cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2RGB)
            axes[i].imshow(img)
            axes[i].set_title(pipeline.name)
            axes[i].axis("off")
        fig.suptitle(row["video_id"])
        out_path = GRID_DIR / f"{row['video_id']}_grid.png"
        fig.tight_layout()
        fig.savefig(out_path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs.append(str(out_path.relative_to(ROOT)))
    return outputs


def simple_features(image_rgb: np.ndarray) -> np.ndarray:
    resized = cv2.resize(image_rgb, (128, 128))
    hsv = cv2.cvtColor(resized, cv2.COLOR_RGB2HSV)
    hist_h = cv2.calcHist([hsv], [0], None, [16], [0, 180]).flatten()
    hist_s = cv2.calcHist([hsv], [1], None, [16], [0, 256]).flatten()
    gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    edge_density = np.array([edges.mean() / 255.0], dtype=np.float32)
    lap_var = np.array([cv2.Laplacian(gray, cv2.CV_32F).var()], dtype=np.float32)
    feat = np.concatenate([hist_h, hist_s, edge_density, lap_var]).astype(np.float32)
    norm = np.linalg.norm(feat) + 1e-8
    return feat / norm


def build_feature_table(frame_index: pd.DataFrame, variant: str) -> tuple[np.ndarray, np.ndarray]:
    features = []
    labels = []
    for _, row in frame_index.iterrows():
        if variant == "raw":
            path = ROOT / row["frame_file"]
        else:
            path = ENHANCED_DIR / variant / row["video_id"] / Path(row["frame_file"]).name
        image_bgr = cv2.imread(str(path))
        if image_bgr is None:
            continue
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        features.append(simple_features(image_rgb))
        labels.append(row["video_id"])
    return np.vstack(features), np.array(labels)


def load_image_variant(row: pd.Series, variant: str) -> np.ndarray | None:
    if variant == "raw":
        path = ROOT / row["frame_file"]
    else:
        path = ENHANCED_DIR / variant / row["video_id"] / Path(row["frame_file"]).name
    image_bgr = cv2.imread(str(path))
    if image_bgr is None:
        return None
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return image_rgb


def build_cnn_table(frame_index: pd.DataFrame, variant: str, image_size: int = 96) -> tuple[np.ndarray, np.ndarray]:
    images = []
    labels = []
    for _, row in frame_index.iterrows():
        image_rgb = load_image_variant(row, variant)
        if image_rgb is None:
            continue
        resized = cv2.resize(image_rgb, (image_size, image_size)).astype(np.float32) / 255.0
        images.append(np.transpose(resized, (2, 0, 1)))
        labels.append(row["video_id"])
    return np.stack(images), np.array(labels)


def split_labels(y: np.ndarray) -> tuple[LabelEncoder, np.ndarray, np.ndarray]:
    label_encoder = LabelEncoder()
    y_enc = label_encoder.fit_transform(y)
    indices = np.arange(len(y_enc))
    train_idx, test_idx = train_test_split(
        indices,
        test_size=0.3,
        random_state=SEED,
        stratify=y_enc,
    )
    return label_encoder, train_idx, test_idx


def cnn_accuracy(
    frame_index: pd.DataFrame,
    variant: str,
    epochs: int = 12,
    batch_size: int = 16,
) -> dict[str, object]:
    X, y = build_cnn_table(frame_index, variant)
    label_encoder, train_idx, test_idx = split_labels(y)
    y_enc = label_encoder.transform(y)

    X_train = torch.tensor(X[train_idx], dtype=torch.float32)
    y_train = torch.tensor(y_enc[train_idx], dtype=torch.long)
    X_test = torch.tensor(X[test_idx], dtype=torch.float32)
    y_test = torch.tensor(y_enc[test_idx], dtype=torch.long)

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=batch_size,
        shuffle=True,
        generator=torch.Generator().manual_seed(SEED),
    )

    model = TinyCNN(num_classes=len(label_encoder.classes_))
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    model.train()
    for _ in range(epochs):
        for xb, yb in train_loader:
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        logits = model(X_test)
        preds = torch.argmax(logits, dim=1).cpu().numpy()

    return {
        "accuracy": float(accuracy_score(y_enc[test_idx], preds)),
        "report": classification_report(
            y_enc[test_idx],
            preds,
            target_names=label_encoder.classes_,
            zero_division=0,
            output_dict=True,
        ),
        "epochs": epochs,
        "batch_size": batch_size,
        "image_size": int(X.shape[-1]),
    }


def run_recognition_baseline(frame_index: pd.DataFrame) -> dict[str, dict[str, object]]:
    metrics: dict[str, dict[str, object]] = {}
    variants = ["raw"] + [pipeline.name for pipeline in PIPELINES]
    for variant in variants:
        X, y = build_feature_table(frame_index, variant)
        label_encoder, train_idx, test_idx = split_labels(y)
        y_enc = label_encoder.transform(y)
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y_enc[train_idx], y_enc[test_idx]
        models = {
            "logreg": LogisticRegression(max_iter=2000),
            "knn": KNeighborsClassifier(n_neighbors=3),
        }
        variant_metrics: dict[str, object] = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            variant_metrics[name] = {
                "accuracy": float(accuracy_score(y_test, preds)),
                "report": classification_report(
                    y_test,
                    preds,
                    target_names=label_encoder.classes_,
                    zero_division=0,
                    output_dict=True,
                ),
            }
        variant_metrics["tinycnn"] = cnn_accuracy(frame_index, variant)
        metrics[variant] = variant_metrics
    return metrics


def main() -> None:
    ensure_dirs()
    frame_index = extract_frames()
    run_pipelines(frame_index)
    grids = build_before_after_grids(frame_index)
    metrics = run_recognition_baseline(frame_index)
    summary = {
        "videos": frame_index["video_id"].nunique(),
        "frames": int(len(frame_index)),
        "pipelines": [pipeline.name for pipeline in PIPELINES],
        "grids": grids,
        "metrics": metrics,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
