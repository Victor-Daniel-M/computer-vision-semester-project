# AGENTS.md

## Purpose

This file is the working project guide for the Computer Vision semester mini-project. It summarizes the assignment, defines the expected outputs, and provides a schema for tracking progress, decisions, changes, and thoughts as the project evolves.

This document is expected to grow over time. It should be updated whenever there is a meaningful change in direction, implementation, dataset preparation, experimentation, reporting, or presentation planning.

## Assignment Summary

- Build a significant computer vision project using course concepts.
- Start from the raw dataset provided on MUELE.
- The dataset consists of 21 video clips of different herbal plants captured under diverse environmental and lighting conditions.
- Inspect the dataset and identify one clear computer vision challenge or motivation.
- Build a task-specific dataset from the raw videos.
- If doing detection or recognition with annotations, annotate the dataset in a suitable format.
- Identify the most suitable image features to enhance or extract for the chosen task.
- Describe the feature enhancement or feature extraction techniques used.
- Build a model for image enhancement, detection, recognition, or another justified vision task.
- Evaluate the model.

## Deliverables

- Report in CVPR format, maximum 10 pages excluding references, submitted as PDF.
- PowerPoint presentation summarizing the project.
- GitHub repository link with reproducible code.
- Report and code uploaded to MUELE.
- Presentation date: 13 June 2026.

## What Success Looks Like

- The task is clearly defined and appropriate for the available dataset.
- The dataset preparation process is documented and reproducible.
- The method choice is justified by the problem and available data.
- Evaluation is credible and clearly explained.
- The report reads like a compact research paper in CVPR style.
- The presentation explains both method and results clearly.

## Recommended Project Framing

Prefer a focused and achievable task over a broad one. The assignment description confirms the capture setup, but it does not provide species or class labels. That means supervised classification should not be assumed unless labels are later created or recovered.

Safer task options include:

- Herbal plant image enhancement under varying lighting conditions
- Video-level herbal plant recognition using provisional per-video identifiers
- Image enhancement followed by weakly supervised recognition
- Feature-based visual analysis or clustering of herbal plant imagery

If reliable plant identity labels become available later, the project can be upgraded to supervised classification. More ambitious tasks like object detection should only be chosen if the dataset quality and annotation effort are manageable.

## Key Constraints And Risks

- The dataset may not come with labels in a ready-to-use format.
- The dataset description does not identify plant classes or species names.
- Frames from the same source video should not leak across train, validation, and test splits.
- The report has a strict 10-page limit, so scope must stay tight.
- If annotations are required, the annotation workload may become the main bottleneck.
- Diverse lighting conditions are both an opportunity and a source of model instability.

## Dataset Reality Check

- The current dataset description only states that there are 21 short smartphone videos of herbal plants collected under diverse lighting conditions and environments.
- This description is not the same as having semantic labels for supervised classification.
- Unless plant identities are supplied later or created manually, the project should avoid claiming species classification.
- Any recognition task should be described honestly as weakly supervised, video-level, or provisional if labels are inferred from the video unit itself.

## Working Assumption

- Current assumption: each video predominantly captures a different plant instance or a visually distinct plant subject.
- Under this assumption, each video can be treated as one provisional label for recognition experiments.
- These are weak labels derived from video identity, not confirmed botanical species labels.
- Any results based on this assumption should be described as video-level or weakly supervised recognition rather than species classification.

## Why This Assumption Is Reasonable

- The dataset contains 21 separate videos rather than one long continuous recording.
- The assignment describes them as videos of herbal plants collected in different conditions and environments.
- A video-level label is a practical way to build a reproducible recognition task from unlabeled raw footage.
- This assumption is strong enough to support experimentation, while still being honest about the limitations of the data.

## How Recognition Would Work Under This Assumption

- Extract frames from each video.
- Assign each frame the provisional label of its source video.
- Train and evaluate a recognition model using these video-level labels.
- Compare recognition performance on raw frames versus enhanced frames.
- Interpret the task as distinguishing visually distinct plant videos, not certifying plant species names.

## Class Notes Incorporated

The following points were captured during class and should guide the project direction:

- Preprocessing or enhancing the images is a valid and expected direction.
- The project should clearly describe the challenge being addressed and the steps taken to solve it.
- Object detection and object recognition were both mentioned as possible task families.

Practical interpretation of these notes:

- Image preprocessing and enhancement are not just optional utilities; they can be part of the core contribution.
- The final report should explicitly connect the identified dataset challenge to each pipeline step.
- Detection remains possible, but only if annotation effort and scene clarity make it realistic.
- Recognition is still possible, but task definition must stay honest if semantic labels are missing.

## Candidate Challenge Statements

Possible challenge statements that fit both the assignment and the class notes:

- Diverse lighting conditions reduce the visibility and consistency of herbal plant features, making recognition difficult.
- Natural background clutter and overlapping leaves make plant localization and recognition difficult.
- Smartphone-captured videos introduce motion blur, viewpoint variation, and inconsistent framing.

Each final project direction should state:

- What the main visual challenge is
- What preprocessing or enhancement steps address that challenge
- What model is used after preprocessing
- How the improvement is evaluated

## Observed Visual Challenges

The frames reviewed so far suggest the dataset contains several real-world outdoor imaging problems that can support an enhancement-focused or weakly supervised vision project.

### 1. Overexposure And Highlight Clipping

- Some frames are strongly overexposed due to direct sunlight.
- Large bright regions lose texture and become nearly white.
- This reduces the visibility of leaves, stems, and fine structure.

Possible enhancement responses:

- Gamma correction
- Highlight suppression
- CLAHE on luminance
- Exposure normalization
- Cropping or masking severely clipped regions

Important limitation:

- Fully saturated white regions may have permanently lost detail and cannot be truly recovered.

### 2. Uneven Lighting

- Different parts of the same frame may be in shadow, partial sun, or direct glare.
- This creates unstable contrast and inconsistent color appearance.

Possible enhancement responses:

- Local contrast enhancement
- Adaptive histogram equalization
- Illumination normalization
- Retinex-style correction

### 3. Background Clutter And Occlusion

- Leaves, stems, soil, bark, and other vegetation often overlap.
- The main plant of interest may not be cleanly isolated.

Possible enhancement responses:

- Region-of-interest cropping
- Saliency-guided selection
- Foreground-background separation
- Edge-aware smoothing to preserve structure

### 4. Scale And Scene Variation

- Some videos appear to show small close-range plants, while others include large tree structures.
- The target object scale and context vary significantly between videos.

Possible enhancement responses:

- Multi-scale feature extraction
- Standardized frame sampling
- Center cropping or patch extraction
- Task reframing toward general plant-scene analysis if identity labels remain unavailable

### 5. Smartphone Capture Artifacts

- Videos may contain motion blur, compression artifacts, and inconsistent framing.
- Camera movement can reduce the usefulness of some frames.

Possible enhancement responses:

- Frame quality filtering
- Deblurring where modest blur exists
- Denoising
- Selecting representative sharp frames instead of using every frame

## Implications For Project Design

- The dataset naturally supports an image enhancement project because several visible challenges are directly linked to image quality.
- Any downstream recognition or retrieval task should ideally compare performance before and after enhancement.
- Evaluation should distinguish between recoverable issues such as uneven illumination and non-recoverable issues such as severe clipping.

## Working Principles

- Keep the project narrow, defensible, and reproducible.
- Document every important assumption.
- Update this file on every meaningful change or thought.
- Tie experiments back to the final CVPR-format report.
- Prefer methods that can be implemented, evaluated, and explained clearly within the project timeline.

## Project Workflow

1. Inspect raw dataset.
2. Define one primary vision task.
3. Decide labels, classes, and split strategy.
4. Build the derived dataset.
5. Choose preprocessing and feature strategy.
6. Train baseline model.
7. Improve with one or more justified changes.
8. Evaluate and compare results.
9. Write report in CVPR format.
10. Prepare presentation.

## Suggested Repository Structure

```text
.
├── AGENTS.md
├── assignment.txt
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── evaluation/
├── reports/
│   ├── cvpr/
│   └── figures/
├── slides/
├── results/
│   ├── metrics/
│   ├── plots/
│   └── predictions/
└── README.md
```

## CVPR Report Expectations

The report should stay aligned with CVPR-style research writing. A practical structure is:

- Title
- Abstract
- Introduction
- Related Work
- Dataset And Problem Definition
- Method / Approach
- Experiments And Evaluation
- Results And Analysis
- Limitations
- Conclusion
- References

Keep the report concise, evidence-driven, and reproducible. Figures and tables should carry real explanatory value.

## Presentation Expectations

- Explain the problem clearly.
- Show dataset creation and preprocessing decisions.
- Summarize the chosen model and why it fits.
- Present quantitative and qualitative results.
- Discuss limitations and possible improvements.

## Update Schema

Use the following schema whenever adding a new progress entry to this file.

```yaml
update:
  date: YYYY-MM-DD
  author: human|agent
  phase: dataset|task-definition|preprocessing|features|training|evaluation|report|slides|repo|other
  type: thought|decision|change|result|risk|next-step
  summary: One-line summary
  details:
    - Short supporting point
    - Short supporting point
  affected_files:
    - path/or/none
  status: proposed|in-progress|done|blocked
  follow_up:
    - Concrete next action
```

## Update Rules

- Add a new entry for every meaningful idea, decision, change, experiment, or result.
- Prefer short, factual entries over long narration.
- If a prior decision changes, record the new decision instead of overwriting history.
- When results are added, include enough context to reproduce them later.
- If blocked, explicitly record the blocker and the next recovery step.

## Running Log

### Entry 001

```yaml
update:
  date: 2026-05-05
  author: agent
  phase: task-definition
  type: change
  summary: Created AGENTS.md as the living project guide for the semester project.
  details:
    - Summarized the assignment requirements from assignment.txt
    - Added deliverables including CVPR-format report, slides, and GitHub code
    - Defined a reusable schema for tracking changes, thoughts, and project progress
  affected_files:
    - AGENTS.md
  status: done
  follow_up:
    - Inspect the raw dataset once it is added locally
    - Choose the primary computer vision task based on data quality and labeling effort
```

### Entry 002

```yaml
update:
  date: 2026-05-05
  author: agent
  phase: dataset
  type: risk
  summary: Refined task recommendations after confirming the dataset description does not provide class labels.
  details:
    - The dataset description specifies capture conditions but does not identify herbal plant species or classes
    - Supervised classification should not be assumed unless labels are supplied later or created manually
    - Recommended reframing toward enhancement, weakly supervised recognition, or feature-based analysis
  affected_files:
    - AGENTS.md
  status: done
  follow_up:
    - Inspect several videos directly to assess scene consistency and dominant subject visibility
    - Decide whether the project should use enhancement, weak supervision, or manual labeling
```

### Entry 003

```yaml
update:
  date: 2026-05-05
  author: agent
  phase: task-definition
  type: change
  summary: Incorporated class notes emphasizing preprocessing, challenge definition, and possible detection or recognition directions.
  details:
    - Added class-note guidance that image preprocessing or enhancement can be part of the main project contribution
    - Added candidate challenge statements tied to lighting variation, clutter, and smartphone capture conditions
    - Clarified that the final report should connect the identified challenge to each pipeline step
  affected_files:
    - AGENTS.md
  status: done
  follow_up:
    - Use the class notes to narrow the final problem statement after a few videos are inspected
    - Prefer a task that allows both a clear challenge description and measurable preprocessing impact
```

### Entry 004

```yaml
update:
  date: 2026-05-05
  author: agent
  phase: dataset
  type: change
  summary: Added observed visual challenges section based on sample frames showing clutter, scale variation, and severe overexposure.
  details:
    - Documented overexposure, uneven lighting, clutter, scale variation, and smartphone capture artifacts
    - Linked each challenge to possible enhancement or preprocessing responses
    - Noted that clipped highlights may be unrecoverable and should be discussed as a limitation
  affected_files:
    - AGENTS.md
  status: done
  follow_up:
    - Inspect a few full videos to verify how common each visual challenge is across the dataset
    - Use the observed challenges to define the final enhancement pipeline
```

### Entry 005

```yaml
update:
  date: 2026-05-05
  author: agent
  phase: task-definition
  type: decision
  summary: Added a working weak-label assumption that each video predominantly represents a distinct plant instance or visually distinct subject.
  details:
    - Defined video identity as a provisional label for recognition experiments
    - Clarified that these are not confirmed species labels
    - Framed the downstream task as weakly supervised video-level recognition
  affected_files:
    - AGENTS.md
  status: done
  follow_up:
    - Verify whether the videos are visually distinct enough to support the assumption
    - Design the frame extraction and split strategy around video-level labels
```

### Entry 006

```yaml
update:
  date: 2026-05-07
  author: agent
  phase: evaluation
  type: result
  summary: Built a proof-of-concept enhancement and weak-recognition pipeline over the 21 videos.
  details:
    - Extracted 218 sampled frames across 21 videos and created a frame-to-video CSV index
    - Implemented three enhancement variants named clahe, balanced, and full
    - Generated before-and-after grids and ran a quick weak-label recognition baseline on raw versus enhanced frames
    - Initial k-NN accuracy was highest on raw frames at about 0.64, with clahe close behind at about 0.62
  affected_files:
    - src/pipeline.py
    - notebooks/poc_review.ipynb
    - outputs/poc/frame_index.csv
    - outputs/poc/reports/summary.json
  status: done
  follow_up:
    - Inspect the generated grids to decide which enhancement pipeline looks most visually useful
    - Replace the simple handcrafted recognition features with stronger pretrained embeddings in the next pass
```

### Entry 007

```yaml
update:
  date: 2026-05-07
  author: agent
  phase: evaluation
  type: result
  summary: Added a tiny CNN baseline and found it underperformed the simpler weak-recognition baselines.
  details:
    - Implemented a lightweight CNN classifier trained on 96x96 frame crops with video-level weak labels
    - The best CNN result was on raw frames at about 0.24 accuracy, below both k-NN and logistic regression
    - Enhancement variants further reduced CNN performance in this first setup, suggesting the dataset is too small for an effective from-scratch CNN baseline
  affected_files:
    - src/pipeline.py
    - outputs/poc/reports/summary.json
  status: done
  follow_up:
    - Try a stronger recognition baseline using pretrained CNN embeddings instead of a from-scratch network
    - Keep raw and clahe as the most plausible variants for the next recognition pass
```

### Entry 008

```yaml
update:
  date: 2026-05-07
  author: agent
  phase: evaluation
  type: result
  summary: Increased frame sampling density and observed clear gains across all recognition baselines.
  details:
    - Raised sampling density to about 1 second intervals with up to 30 frames per video, increasing the working set to 469 frames
    - Raw-frame k-NN improved from about 0.64 to about 0.82 accuracy, and raw logistic regression improved from about 0.47 to about 0.63
    - The tiny CNN improved from about 0.24 to about 0.39 on raw frames, showing that additional frame diversity helps the learned model even though it still trails the simpler baselines
  affected_files:
    - src/pipeline.py
    - outputs/poc/frame_index.csv
    - outputs/poc/reports/summary.json
  status: done
  follow_up:
    - Decide whether to keep the denser sampling as the default POC setting
    - Try pretrained CNN embeddings next, since the larger sample appears to support stronger models better
```

### Entry 009

```yaml
update:
  date: 2026-05-11
  author: agent
  phase: evaluation
  type: result
  summary: Added pretrained ResNet18 embeddings and found enhanced variants that beat raw recognition accuracy.
  details:
    - Added lighter enhancement variants named clahe_light, gamma_light, gamma_clahe_light, and sharpen_light while keeping clahe
    - Added ResNet18 feature extraction followed by logistic regression and k-NN classifiers
    - The best enhanced variants were clahe and gamma_light at about 0.922 accuracy with ResNet18 logistic regression, compared with raw at about 0.915
    - The pretrained weights are cached locally under outputs/poc/torch_cache and ignored by git
  affected_files:
    - src/pipeline.py
    - outputs/poc/reports/summary.json
    - outputs/poc/reports/accuracy_table.csv
    - .gitignore
  status: done
  follow_up:
    - Inspect before-and-after grids for clahe and gamma_light to choose the most defensible enhancement method
    - Use ResNet18 logistic regression as the stronger weak-recognition baseline in the report
```

## Next Recommended Additions

- Dataset inventory summary after reviewing the raw videos
- Candidate project ideas with tradeoffs
- Final task definition
- Data split policy
- Baseline model plan
- Report outline in CVPR format
- Slide outline
