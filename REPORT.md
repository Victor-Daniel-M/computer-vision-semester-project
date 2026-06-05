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

Image enhancement is a common preprocessing step in computer vision when images suffer from low contrast, uneven illumination, blur, or sensor artifacts. Histogram equalization improves global contrast by redistributing intensity values, but it can over-amplify noise when applied uniformly. CLAHE addresses this by applying adaptive histogram equalization locally while limiting contrast amplification [1].

Gamma correction is another simple enhancement technique. It applies a nonlinear tone mapping that can brighten or darken midtones without changing the image uniformly [2]. This makes it useful for smartphone imagery where exposure may be inconsistent.

Sharpening is also a standard spatial-domain enhancement operation for improving apparent edge definition and local detail [2]. In this project, sharpening is used conservatively because plant recognition depends on fine leaf and stem structures, but excessive sharpening can amplify compression artifacts and noise.

More advanced enhancement methods also exist. Retinex-based methods model an image as a combination of illumination and reflectance, making them well suited to illumination correction and color constancy problems [6]. Recent deep low-light enhancement methods build on this idea and can produce stronger perceptual results, but they often require additional training data, paired or unpaired enhancement datasets, or more complex validation [7]. Because this dataset is small, weakly labeled, and collected specifically for a course project, this work uses CLAHE, gamma correction, and mild sharpening as interpretable, reproducible classical enhancement baselines rather than claiming they are the most advanced possible enhancement methods.

Deep convolutional networks are widely used for recognition, but training CNNs from scratch usually requires large labeled datasets. In this project, enhancement is evaluated through a progression of recognition baselines: handcrafted features with logistic regression and k-nearest neighbors, a Tiny CNN trained from scratch, and finally ResNet18 embeddings with logistic regression and k-nearest neighbors. The handcrafted baselines provide simple color, edge, and sharpness comparisons; the Tiny CNN provides a lightweight learned baseline; and ResNet18 embeddings [3] provide the stronger pretrained representation for testing whether enhancement improves downstream recognition without requiring large-scale training.

## 3. Dataset and Problem Definition

The raw dataset contains 21 short videos of herbal plants captured with a smartphone camera under diverse lighting conditions and environments. The provided assignment description does not include botanical labels or bounding-box annotations. Therefore, this project does not claim expert species classification.

Instead, the project uses the following working assumption:

**Each video predominantly captures a distinct plant instance or visually distinct plant subject.**

Under this assumption, frames extracted from the same video inherit the same provisional video-level label. This creates a weakly supervised recognition task because the supervision is coarse and derived from the video unit rather than verified independently for every frame [4]. Similar video-level labeling strategies are common in video recognition datasets, but they introduce frame-level uncertainty because not every frame necessarily contains the same discriminative visual evidence [5]. In this project, the resulting task is: given a frame, the system predicts which source video or plant subject it most likely belongs to.

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

Frames are sampled at approximately one-second intervals, with a cap of 30 frames per video. The cap is not reached by every video because several clips are shorter than 30 seconds; in the extracted dataset, per-video frame counts range from 12 to 30. This produces 469 sampled frames from 21 videos. Each frame is indexed in a CSV file with its source video, frame index, timestamp, and path.

### 4.2 Enhancement Variants

The following image variants are evaluated:

- `raw`: original extracted frames without enhancement.
- `clahe`: CLAHE applied to the luminance channel.
- `clahe_light`: CLAHE with a lower clip limit for gentler local contrast enhancement.
- `gamma_light`: mild gamma correction with gamma set to 1.08.
- `gamma_clahe_light`: mild gamma correction followed by light CLAHE.
- `sharpen_light`: mild unsharp masking for detail enhancement.

CLAHE improves local contrast while limiting noise amplification. Gamma correction adjusts image tone nonlinearly and can improve midtone visibility without drastically changing color or texture. Mild sharpening tests whether clearer edges and leaf boundaries improve recognition features. These methods are common classical enhancement operations and are appropriate first choices because they are simple, fast, explainable, and do not require enhancement-specific training labels. The lighter variants are intentionally conservative so the pipeline can test whether small tonal changes help without heavily altering plant color and texture cues.

### 4.3 Recognition Baselines

Recognition is used as the downstream evaluation task: if an enhancement method makes plant frames more visually informative, a recognition model should perform at least slightly better on enhanced frames than on raw frames. To avoid relying on a single model, three recognition families are tested:

- Handcrafted features: HSV color histograms, edge density, and Laplacian sharpness variance are extracted from each frame. These features are evaluated with logistic regression and 3-nearest neighbors. This baseline tests whether enhancement improves simple color, edge, and sharpness cues commonly used in classical image analysis [2], while k-nearest neighbors provides a simple non-parametric recognition baseline [8].
- Tiny CNN: a small three-layer convolutional network is trained from scratch on 96x96 frame crops for 12 epochs. This baseline tests whether a lightweight learned model can benefit from enhancement, while also showing the limitation of training a CNN from a small weakly labeled dataset. CNNs are a standard architecture for visual recognition because convolutional layers learn local spatial patterns such as edges, textures, and shapes [9].
- ResNet18 embeddings: pretrained ResNet18 is used as a fixed feature extractor, and the resulting embeddings are classified using logistic regression and 3-nearest neighbors. This baseline tests enhancement using stronger visual features learned from large-scale image pretraining. Using pretrained CNN activations as general-purpose visual features is a common transfer-learning strategy for small recognition datasets [10].

All baselines use the same stratified 70/30 frame-level train-test split so that raw and enhanced variants are compared under the same evaluation conditions. The strongest recognition setup is ResNet18 feature extraction followed by logistic regression, so it is used as the main result for judging whether enhancement improves downstream recognition.

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

However, not all enhancement helps. In the current ResNet18-logistic regression results, `clahe_light` and `gamma_clahe_light` reach 90.78%, below the raw-frame baseline of 91.49%, while `sharpen_light` only matches raw performance. This suggests that enhancement is useful only when it improves visibility without changing the cues used for recognition. Plant recognition depends on subtle color, texture, and shape cues, so overprocessing or combining multiple operations can change those cues enough to hurt classification.

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

[1] K. Zuiderveld. Contrast Limited Adaptive Histogram Equalization. In P. S. Heckbert, editor, *Graphics Gems IV*, pages 474-485. Academic Press, 1994.

[2] R. C. Gonzalez and R. E. Woods. *Digital Image Processing*. 4th edition. Pearson, 2018.

[3] K. He, X. Zhang, S. Ren, and J. Sun. Deep Residual Learning for Image Recognition. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 770-778, 2016.

[4] Z.-H. Zhou. A Brief Introduction to Weakly Supervised Learning. *National Science Review*, 5(1):44-53, 2018.

[5] A. Karpathy, G. Toderici, S. Shetty, T. Leung, R. Sukthankar, and L. Fei-Fei. Large-Scale Video Classification with Convolutional Neural Networks. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 1725-1732, 2014.

[6] E. H. Land and J. J. McCann. Lightness and Retinex Theory. *Journal of the Optical Society of America*, 61(1):1-11, 1971.

[7] W. Yang, S. Wang, Y. Fang, Y. Wang, and J. Liu. From Unpaired to Paired: A Benchmark and Baseline for Low-Light Image Enhancement. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 220-229, 2020.

[8] T. M. Cover and P. E. Hart. Nearest Neighbor Pattern Classification. *IEEE Transactions on Information Theory*, 13(1):21-27, 1967.

[9] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. Gradient-Based Learning Applied to Document Recognition. *Proceedings of the IEEE*, 86(11):2278-2324, 1998.

[10] A. S. Razavian, H. Azizpour, J. Sullivan, and S. Carlsson. CNN Features Off-the-Shelf: An Astounding Baseline for Recognition. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, pages 806-813, 2014.
