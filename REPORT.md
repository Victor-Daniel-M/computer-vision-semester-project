# Enhancing Smartphone-Captured Herbal Plant Video Frames for Weakly Supervised Recognition

## Abstract

Outdoor plant imagery captured with smartphone cameras often contains uneven illumination, cluttered backgrounds, motion blur, and overexposed regions. These conditions make visual analysis difficult, especially when the available data is limited and does not contain expert class labels. This project investigates image enhancement as a preprocessing step for plant video frames collected under diverse environmental and lighting conditions. From 21 short videos of herbal plants, we extract frame samples and use source-video identity as a weak label for recognition experiments. We compare raw frames against several enhancement variants, including Contrast Limited Adaptive Histogram Equalization (CLAHE), light gamma correction, light CLAHE, combined light gamma and CLAHE, and mild sharpening. Recognition is evaluated using handcrafted features, a small CNN trained from scratch, and pretrained ResNet18 embeddings followed by simple classifiers. The best enhanced variants, CLAHE and light gamma correction, improve ResNet18-logistic regression accuracy from 91.49% on raw frames to 92.20%. These results suggest that mild enhancement can improve weak plant recognition, while overly aggressive enhancement may distort useful visual cues.

## 1. Introduction

Computer vision systems often assume that images are clear, well-lit, and consistently framed. In practical field conditions, this assumption is fragile. Plant videos captured outdoors with a smartphone may contain strong sunlight, shadows, background vegetation, soil, bark, blur, and large changes in scale. These issues are visible in the provided dataset and directly affect the reliability of recognition.

The project assignment requires identifying a computer vision challenge in a dataset of 21 herbal plant videos collected under diverse lighting and environmental conditions. Since the dataset description does not provide semantic species labels, this work treats the problem as an image enhancement and weakly supervised recognition task rather than strict species classification. The central question is:

**Can lightweight image enhancement improve recognition of plant video frames under weak video-level labels?**

The main contributions of this project are:

- A reproducible frame extraction pipeline from raw smartphone videos.
- A set of lightweight enhancement pipelines designed for outdoor plant imagery.
- A weak-label recognition setup using source-video identity as the provisional label.
- An empirical comparison of raw and enhanced frames using classical features, a small CNN, and pretrained ResNet18 embeddings.

## 2. Related Work

Image enhancement is a common preprocessing step in computer vision when images suffer from low contrast, uneven illumination, blur, or sensor artifacts. Histogram equalization improves global contrast by redistributing intensity values, but it can over-amplify noise when applied uniformly. CLAHE addresses this by applying adaptive histogram equalization locally while limiting contrast amplification.

Gamma correction is another simple enhancement technique. It applies a nonlinear tone mapping that can brighten or darken midtones without changing the image uniformly. This makes it useful for smartphone imagery where exposure may be inconsistent.

Deep convolutional networks are widely used for recognition, but training CNNs from scratch usually requires large labeled datasets. In small-data settings, pretrained CNNs are often used as feature extractors. This project uses ResNet18 embeddings to evaluate whether enhancement improves downstream recognition without needing to train a deep model from scratch.

## 3. Dataset and Problem Definition

The raw dataset contains 21 short videos of herbal plants captured with a smartphone camera under diverse lighting conditions and environments. The provided assignment description does not include botanical labels or bounding-box annotations. Therefore, this project does not claim expert species classification.

Instead, the project uses the following working assumption:

**Each video predominantly captures a distinct plant instance or visually distinct plant subject.**

Under this assumption, frames extracted from the same video inherit the same provisional video-level label. This creates a weakly supervised recognition task: given a frame, the system predicts which source video or plant subject it most likely belongs to.

### 3.1 Observed Visual Challenges

Initial inspection showed several visual challenges:

- Overexposure and clipped highlights caused by direct sunlight.
- Uneven illumination across the same frame.
- Background clutter from soil, bark, stems, and surrounding vegetation.
- Scale variation, including close-up herbs and larger tree structures.
- Smartphone capture artifacts such as blur, compression, and inconsistent framing.

These observations motivate an enhancement-focused pipeline.

## 4. Method

The project pipeline has four main stages:

1. Extract frames from each raw video.
2. Apply image enhancement variants to each extracted frame.
3. Extract recognition features from raw and enhanced frames.
4. Compare recognition accuracy across variants.

### 4.1 Frame Extraction

Frames are sampled at approximately one-second intervals, with up to 30 frames per video. This produces 469 sampled frames from 21 videos. Each frame is indexed in a CSV file with its source video, frame index, timestamp, and path.

### 4.2 Enhancement Variants

The following image variants are evaluated:

- `raw`: original extracted frames without enhancement.
- `clahe`: CLAHE applied to the luminance channel.
- `clahe_light`: CLAHE with a lower clip limit for gentler local contrast enhancement.
- `gamma_light`: mild gamma correction with gamma set to 1.08.
- `gamma_clahe_light`: mild gamma correction followed by light CLAHE.
- `sharpen_light`: mild unsharp masking for detail enhancement.

CLAHE improves local contrast while limiting noise amplification. Gamma correction adjusts image tone nonlinearly and can improve midtone visibility without drastically changing color or texture. The lighter variants are intentionally conservative because earlier experiments showed that aggressive enhancement can reduce recognition accuracy.

### 4.3 Recognition Baselines

Three recognition families are tested:

- Handcrafted features: HSV color histograms, edge density, and Laplacian sharpness variance.
- Tiny CNN: a small convolutional network trained from scratch on 96x96 frame crops.
- ResNet18 embeddings: pretrained ResNet18 used as a fixed feature extractor, followed by logistic regression or k-nearest neighbors.

The strongest recognition setup is ResNet18 feature extraction followed by logistic regression.

## 5. Experiments

The evaluation uses a weak video-level recognition setup. Frames are assigned labels according to their source video. The data is split into training and testing sets with stratification by video identity.

The main metric is classification accuracy on the held-out frame set. Accuracy is compared across raw and enhanced frame variants.

Important limitation: this is a frame-level split, not a full video-level holdout. Since frames from the same video can be visually similar, the current results should be interpreted as a proof of concept for weak recognition rather than a final claim of species-level generalization.

## 6. Results

Table 1 summarizes the top recognition results.

| Variant | Model | Accuracy |
|---|---:|---:|
| `clahe` | ResNet18 + Logistic Regression | 0.921986 |
| `gamma_light` | ResNet18 + Logistic Regression | 0.921986 |
| `raw` | ResNet18 + Logistic Regression | 0.914894 |
| `sharpen_light` | ResNet18 + Logistic Regression | 0.914894 |
| `clahe_light` | ResNet18 + Logistic Regression | 0.907801 |
| `gamma_clahe_light` | ResNet18 + Logistic Regression | 0.907801 |
| `raw` | k-NN on handcrafted features | 0.815603 |
| `sharpen_light` | k-NN on handcrafted features | 0.808511 |

The strongest result is achieved by two enhanced variants: `clahe` and `gamma_light`, each reaching 92.20% accuracy. The raw ResNet18 baseline reaches 91.49%. This shows a small but meaningful improvement from mild enhancement.

The small CNN trained from scratch performs substantially worse than the ResNet18 embedding approach. This is expected because the dataset is small and weakly labeled. The pretrained feature extractor provides stronger visual representations without requiring large-scale training.

## 7. Analysis

The results suggest that mild enhancement is more useful than aggressive enhancement for this dataset. CLAHE improves local contrast and may help reveal leaf, stem, and texture details in uneven lighting. Light gamma correction provides a gentler tonal adjustment that preserves visual identity cues while improving brightness distribution.

The improvement over raw frames is modest but important for the project objective. It supports the claim that enhancement can improve weak plant recognition when paired with a strong feature extractor.

However, not all enhancement helps. Earlier and current experiments show that stronger enhancement or combinations of multiple operations can reduce recognition performance. This likely happens because plant recognition depends on subtle color, texture, and shape cues. Overprocessing can change these cues enough to hurt classification.

## 8. Limitations

This project has several limitations:

- The labels are weak video-level labels, not expert botanical species labels.
- The current split is frame-level, so similar frames from one video may appear across training and testing.
- Severe overexposure cannot fully recover information lost in saturated white regions.
- The dataset is small, with only 21 videos.
- The current analysis focuses on recognition accuracy and does not yet include full no-reference image quality metrics.

## 9. Conclusion

This project investigates image enhancement for smartphone-captured herbal plant videos under diverse outdoor conditions. Because the dataset lacks semantic labels, the project is framed as weakly supervised video-level recognition. The experiments show that mild enhancement methods can improve recognition when paired with pretrained ResNet18 embeddings. Specifically, CLAHE and light gamma correction outperform the raw-frame baseline, increasing accuracy from 91.49% to 92.20%.

The findings support the use of conservative image enhancement as a preprocessing step for plant image analysis. Future work should evaluate stronger split strategies, add image quality metrics, and explore whether manually verified plant labels can support true species-level recognition.

## References

TODO: Add formal references in CVPR style.

Candidate references:

- K. He, X. Zhang, S. Ren, and J. Sun. Deep Residual Learning for Image Recognition. CVPR, 2016.
- OpenCV documentation for histogram equalization and CLAHE.
- R. C. Gonzalez and R. E. Woods. Digital Image Processing.

