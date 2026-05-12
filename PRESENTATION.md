# Presentation Outline

## Slide 1: Title

**Enhancing Smartphone-Captured Herbal Plant Video Frames for Weakly Supervised Recognition**

Computer Vision Mini Project

Presenter: Victor

## Slide 2: Motivation

Outdoor plant videos are visually challenging because they contain:

- Uneven lighting
- Strong sunlight and shadows
- Overexposed regions
- Dense vegetation and clutter
- Motion blur and smartphone capture artifacts

Goal:

**Improve plant frame visibility and test whether enhancement improves weak recognition.**

## Slide 3: Dataset

Dataset provided on MUELE:

- 21 short videos
- Herbal plant imagery
- Captured using a smartphone camera
- Diverse lighting conditions and environments

Important constraint:

- No expert species labels were provided.
- No bounding-box annotations were provided.

## Slide 4: Problem Framing

Because the dataset has no semantic labels, the project is framed as:

**Image enhancement + weakly supervised video-level recognition**

Working assumption:

- Each video mostly captures one distinct plant instance or visually distinct plant subject.
- Frames inherit the identity of their source video as a weak label.

This is not botanical species classification.

## Slide 5: Observed Visual Challenges

Examples to show:

- Overexposed plant frame
- Cluttered herb/leaf frame
- Tree or large-scale plant frame
- Uneven illumination frame

Key message:

The dataset naturally supports an enhancement-focused computer vision task.

## Slide 6: Pipeline Overview

Pipeline:

1. Extract frames from raw videos.
2. Apply enhancement variants.
3. Extract visual features.
4. Train weak-label recognizers.
5. Compare raw vs enhanced accuracy.

Current extracted dataset:

- 469 sampled frames
- 21 weak video-level classes

## Slide 7: Enhancement Methods

Tested image variants:

- `raw`: no enhancement
- `clahe`: local contrast enhancement
- `clahe_light`: gentler local contrast enhancement
- `gamma_light`: mild tonal correction
- `gamma_clahe_light`: light gamma + light CLAHE
- `sharpen_light`: mild sharpening

Main idea:

Use conservative enhancement to improve visibility without destroying plant identity cues.

## Slide 8: What Is CLAHE?

CLAHE = Contrast Limited Adaptive Histogram Equalization.

What it does:

- Enhances local contrast
- Works well when one image contains both shadow and bright regions
- Limits contrast amplification to avoid excessive noise

Why it fits this dataset:

- Leaves, stems, bark, and flowers often appear under uneven lighting.
- Local contrast can make plant structures more visible.

## Slide 9: What Is Gamma Light?

`gamma_light` is mild gamma correction.

What it does:

- Applies a gentle nonlinear brightness adjustment
- Changes image tone without heavily altering color or texture
- Helps midtones become more usable

Why it fits this dataset:

- Smartphone exposure varies across videos.
- Some frames need light tonal correction rather than heavy enhancement.

## Slide 10: Recognition Setup

Recognition baselines:

- Handcrafted features + k-NN / logistic regression
- Tiny CNN trained from scratch
- Pretrained ResNet18 embeddings + k-NN / logistic regression

Best setup:

**ResNet18 embeddings + logistic regression**

Why:

- ResNet18 provides strong visual features.
- Logistic regression is simple and reproducible.
- No need to train a large CNN from scratch.

## Slide 11: Main Results

Top results:

| Variant | Model | Accuracy |
|---|---:|---:|
| `clahe` | ResNet18 + Logistic Regression | 0.921986 |
| `gamma_light` | ResNet18 + Logistic Regression | 0.921986 |
| `raw` | ResNet18 + Logistic Regression | 0.914894 |
| `sharpen_light` | ResNet18 + Logistic Regression | 0.914894 |

Key result:

**CLAHE and gamma_light outperform raw frames.**

## Slide 12: Interpretation

What the results suggest:

- Mild enhancement can improve weak plant recognition.
- Aggressive enhancement is not automatically better.
- Pretrained features are much stronger than a small CNN trained from scratch.
- Enhancement must preserve discriminative plant cues such as color, texture, and structure.

## Slide 13: Limitations

Current limitations:

- Labels are weak video-level labels.
- No expert plant species labels are available.
- Current split is frame-level, so similar frames may appear in train and test.
- Severe overexposure cannot fully recover lost image detail.
- Dataset is small.

## Slide 14: Conclusion

Summary:

- Built a reproducible enhancement and recognition pipeline.
- Extracted frames from 21 smartphone plant videos.
- Tested multiple image enhancement methods.
- Found that CLAHE and light gamma correction improve recognition over raw frames.

Main conclusion:

**Conservative image enhancement can improve weakly supervised recognition of smartphone-captured plant video frames.**

## Slide 15: Future Work

Possible improvements:

- Add manual plant labels if species identities become available.
- Use a stronger split strategy based on video segments.
- Add image quality metrics such as contrast, entropy, blur, and clipping.
- Compare more pretrained models.
- Convert the final report to CVPR format and add polished figures.

