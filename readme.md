# Boxing App

A real-time boxing game that uses webcam-based pose detection to track punches and blocks, with a stamina and health system driving the core gameplay loop.

## How It Works

The game captures webcam frames, runs them through a YOLO pose detection model to extract body keypoints (shoulders, elbows, wrists), and uses the geometry of those keypoints to detect two core actions:

- **Punches** — detected via elbow angle combined with the wrist entering a defined "punch zone" on screen
- **Blocks** — detected via both wrists being raised above the nose/head keypoint

These feed into a stamina system (punching and blocking both drain stamina at different rates, with passive regeneration) and a health system that will eventually respond to incoming hits.

## Tech Stack

- **YOLO pose model** (Ultralytics) for keypoint detection
- **ONNX Runtime** for optimized inference — the model is exported to ONNX and run through a hand-written preprocessing/inference/decoding pipeline for better performance than the default PyTorch inference path
- **OpenCV** for webcam capture and on-screen rendering

## Performance

The project went through a deliberate optimization pass to get real-time performance on CPU:

| Configuration | Inference Time | Approx. FPS |
|---|---|---|
| yolo26s-pose, 640px, PyTorch | ~145ms | ~7 FPS |
| yolo26s-pose, 640px, ONNX | ~145ms | ~7 FPS |
| yolo26n-pose, 640px, ONNX | ~65ms | ~14 FPS |
| yolo26s-pose, 416px, ONNX | ~65ms | ~14 FPS |
| **yolo26n-pose, 416px, ONNX** | **~31ms** | **~28 FPS** |

Key optimizations:
- Switched from the `.pt` model to a raw ONNX export with hand-written pre/post-processing (skipping Ultralytics' wrapper overhead)
- Swapped from the "small" to the "nano" YOLO pose variant
- Reduced input resolution from 640px to 416px
- Limited `max_det` to reduce unnecessary candidate detections

## Project Structure

```
game/       - core gameplay logic (punch/block detection, stamina, health)
models/     - ONNX export scripts and inference pipeline
```

## Status

Currently a single-player local prototype — punch/block detection, stamina, and health systems are functional. Multiplayer networking is planned but not yet part of this build.

## Setup

```bash
pip install ultralytics opencv-python onnxruntime
python models/onnx_export.py   # exports the pose model to ONNX
python game/main.py            # runs the game
```