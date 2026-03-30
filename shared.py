from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GameMode(str, Enum):
    FLAPPY = "flappy"
    MARIO = "mario"
    SNAKE = "snake"
    PACMAN = "pacman"


@dataclass
class GestureEvent:
    head: str = "CENTER"  # LEFT RIGHT UP DOWN CENTER
    blink: bool = False
    left_wink: bool = False
    right_wink: bool = False
    eyebrow_raise: bool = False
    pause: bool = False
    resume: bool = False


GAME_PATHS = {
    GameMode.FLAPPY: "Games/FlappyBird/flappy.py",
    GameMode.MARIO: "Games/SuperMario/main.py",
    GameMode.SNAKE: "Games/og_snake.py",
    GameMode.PACMAN: "Games/PacMan/pacman.py",
}
