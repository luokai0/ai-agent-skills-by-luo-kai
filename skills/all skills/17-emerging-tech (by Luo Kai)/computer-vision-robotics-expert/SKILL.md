---
name: computer-vision-robotics-expert
version: 1.0.0
description: Expert-level computer vision for robotics covering camera models, feature detection, object detection, pose estimation, visual SLAM, and deep learning for perception.
author: luo-kai
tags: [computer vision, robotics, SLAM, object detection, pose estimation, deep learning]
---

# Computer Vision Robotics Expert

## Before Starting
1. RGB, depth, or stereo camera?
2. Detection, pose estimation, or SLAM?
3. Classical or deep learning approach?

## Core Expertise Areas

### Camera Models
Pinhole camera: projects 3D point to 2D image plane through focal point.
Intrinsic matrix K: focal lengths and principal point, 5 parameters.
Distortion: radial and tangential lens distortion, correct before processing.
Stereo camera: two calibrated cameras, disparity gives depth.
Depth cameras: structured light or time-of-flight, direct depth measurement.

### Feature Detection
Corners: Harris detector, stable under rotation, used for tracking.
SIFT: scale and rotation invariant features, robust but slow.
ORB: binary features, fast, used in real-time SLAM.
Feature matching: descriptor distance, ratio test, RANSAC for outlier rejection.

### Object Detection
Classical: HOG plus SVM, sliding window, deformable parts model.
YOLO: single-shot detector, real-time, divides image into grid.
Faster R-CNN: region proposal network, accurate but slower.
Segmentation: semantic labels per pixel, instance segmentation separates objects.

### Visual SLAM
SLAM: simultaneous localization and mapping, build map while tracking position.
Visual odometry: estimate motion from consecutive image frames.
Loop closure: detect revisited places, correct accumulated drift.
ORB-SLAM3: feature-based, monocular and RGB-D, open-source reference system.
NERF and 3DGS: neural radiance fields for photorealistic scene reconstruction.

## Best Practices
- Calibrate cameras carefully before any metric reconstruction task
- Use data augmentation to improve detection robustness
- Test perception system under lighting variation and occlusion
- Validate pose estimation with ground truth before deployment

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Skipping camera calibration | Always calibrate, reprojection error should be below 1 pixel |
| Ignoring lighting variation | Test and train under diverse lighting conditions |
| Assuming static scene in SLAM | Handle dynamic objects explicitly |
| Overconfident pose estimates | Always provide uncertainty with pose estimates |

## Related Skills
- path-planning-expert
- robot-kinematics-expert
- deep-learning-expert
