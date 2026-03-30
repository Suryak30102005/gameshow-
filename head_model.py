from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeadModel:
    """Small heuristic fallback head-direction model.

    The production PRD references a trained sklearn model; this fallback keeps
    the same interface and can be swapped with a persisted estimator later.
    """

    left_threshold: float = -0.18
    right_threshold: float = 0.18
    up_threshold: float = -0.12
    down_threshold: float = 0.14

    def predict_direction(self, yaw: float, pitch: float) -> str:
        if yaw < self.left_threshold:
            return "LEFT"
        if yaw > self.right_threshold:
            return "RIGHT"
        if pitch < self.up_threshold:
            return "UP"
        if pitch > self.down_threshold:
            return "DOWN"
        return "CENTER"
