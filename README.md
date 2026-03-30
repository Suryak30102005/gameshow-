# FacePlay

FacePlay is a hands-free game controller and game suite that uses webcam gestures and voice commands.

## Implemented in this repository

- Tkinter launcher with game cards and optional voice selection.
- Controller process with five-step calibration flow.
- Gesture abstraction layer with webcam provider stub and keyboard fallback provider.
- Four playable Pygame games:
  - Flappy Bird clone (`Games/FlappyBird/flappy.py`)
  - Super Mario-inspired side runner (`Games/SuperMario/main.py`)
  - OG Snake (`Games/og_snake.py`)
  - Pac-Man-inspired maze runner (`Games/PacMan/pacman.py`)
- Auto pause / resume command channel between controller and game.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python launcher.py
```

## Controls (fallback mode)

If webcam/voice dependencies are unavailable, FacePlay can be used with keyboard simulation in calibration/gameplay windows.

- Arrow keys = head directions
- `b` = blink
- `q` = left wink
- `e` = right wink
- `r` = eyebrow raise (hold supported)
- `p` = pause, `o` = resume

This fallback is intended for development and testing.
