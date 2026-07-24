# Gesture-Controlled Music Player (macOS)

Control music playback with hand gestures using your webcam, no mouse or keyboard needed.

## Features
- **Pinch** (thumb + index finger together) → play/pause
- **Point left / right** (index finger relative to wrist) → previous / next track
- **Raise / lower hand** → volume up / down

## How it works
Uses [MediaPipe](https://developers.google.com/mediapipe) to track 21 hand landmarks in real time from webcam input, then applies distance and position calculations between specific landmarks to detect each gesture. Detected gestures trigger macOS media key presses (via `pynput`) and system volume changes (via `osascript`), so it works with any macOS media app (tested with Spotify).

## Tech stack
Python, OpenCV, MediaPipe, pynput

## Setup
1. Clone the repo
2. `pip install opencv-python mediapipe pynput`
3. `python3 main.py`
4. Grant camera + accessibility permissions when prompted (macOS)
5. Open Spotify (or any media app) and start playing something — pinch, point, or raise your hand to control it
