from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame

from shared import GameMode, GestureEvent

STATE_FILE = Path(".faceplay_state.json")


@dataclass
class CalibrationProfile:
    neutral_ear: float
    blink_threshold: float
    left_wink_threshold: float
    right_wink_threshold: float
    eyebrow_threshold: float


def run_calibration() -> CalibrationProfile:
    print("Starting 5-step calibration (development mode)")
    print("Press ENTER to progress each calibration step.")
    input("1) Neutral eye openness captured. Press ENTER...")
    input("2) Full blink threshold captured. Press ENTER...")
    input("3) Left wink threshold captured. Press ENTER...")
    input("4) Right wink threshold captured. Press ENTER...")
    input("5) Eyebrow raise threshold captured. Press ENTER...")
    return CalibrationProfile(0.25, 0.18, 0.2, 0.2, 0.35)


def write_state(mode: GameMode, event: GestureEvent) -> None:
    payload = {"mode": mode.value, "event": asdict(event), "ts": time.time()}
    STATE_FILE.write_text(json.dumps(payload), encoding="utf-8")


def keyboard_provider() -> GestureEvent:
    event = GestureEvent()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        event.head = "LEFT"
    elif keys[pygame.K_RIGHT]:
        event.head = "RIGHT"
    elif keys[pygame.K_UP]:
        event.head = "UP"
    elif keys[pygame.K_DOWN]:
        event.head = "DOWN"
    if keys[pygame.K_b]:
        event.blink = True
    if keys[pygame.K_q]:
        event.left_wink = True
    if keys[pygame.K_e]:
        event.right_wink = True
    if keys[pygame.K_r]:
        event.eyebrow_raise = True
    if keys[pygame.K_p]:
        event.pause = True
    if keys[pygame.K_o]:
        event.resume = True
    return event


def control_loop(mode: GameMode) -> None:
    pygame.init()
    pygame.display.set_caption("FacePlay Controller (Fallback Keyboard Mode)")
    screen = pygame.display.set_mode((760, 180))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        event = keyboard_provider()
        write_state(mode, event)

        screen.fill((20, 20, 30))
        rows = [
            "Fallback controls: arrows=head, b=blink, q/e=winks, r=eyebrow",
            "p=pause, o=resume. Keep this window open while playing.",
            f"Detected: head={event.head}, blink={event.blink}, eyebrow={event.eyebrow_raise}",
        ]
        y = 25
        for row in rows:
            txt = font.render(row, True, (220, 220, 220))
            screen.blit(txt, (18, y))
            y += 40

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=[m.value for m in GameMode], required=True)
    parser.add_argument("--skip-calibration", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mode = GameMode(args.mode)
    if not args.skip_calibration:
        profile = run_calibration()
        os.environ["FACEPLAY_CALIBRATION"] = json.dumps(asdict(profile))
    control_loop(mode)


if __name__ == "__main__":
    main()
