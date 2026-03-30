from __future__ import annotations

import random
import time

import pygame

from Games.common import event_recent, read_event

W, H = 620, 620
CELL = 20
GRID = W // CELL


def random_cell() -> tuple[int, int]:
    return random.randint(1, GRID - 2), random.randint(1, GRID - 2)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('FacePlay - PacMan')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    pac = [GRID // 2, GRID // 2]
    ghost = [5, 5]
    pellets = {random_cell() for _ in range(70)}
    score = 0
    over = False
    blink_hold_start: float | None = None

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        payload = read_event()
        ge = payload.get('event', {}) if event_recent(payload) else {}

        if ge.get('blink'):
            if blink_hold_start is None:
                blink_hold_start = time.time()
            if time.time() - blink_hold_start > 3:
                break
        else:
            blink_hold_start = None

        if over and ge.get('blink'):
            pac = [GRID // 2, GRID // 2]
            ghost = [5, 5]
            pellets = {random_cell() for _ in range(70)}
            score = 0
            over = False

        if not over:
            head = ge.get('head', 'CENTER')
            if head == 'LEFT':
                pac[0] -= 1
            elif head == 'RIGHT':
                pac[0] += 1
            elif head == 'UP':
                pac[1] -= 1
            elif head == 'DOWN':
                pac[1] += 1

            pac[0] = max(0, min(GRID - 1, pac[0]))
            pac[1] = max(0, min(GRID - 1, pac[1]))
            pellets.discard((pac[0], pac[1]))
            score = 70 - len(pellets)

            ghost_speed = 1
            if ge.get('eyebrow_raise'):
                ghost_speed = 0
            if ghost_speed:
                if ghost[0] < pac[0]:
                    ghost[0] += 1
                elif ghost[0] > pac[0]:
                    ghost[0] -= 1
                elif ghost[1] < pac[1]:
                    ghost[1] += 1
                elif ghost[1] > pac[1]:
                    ghost[1] -= 1

            if tuple(ghost) == tuple(pac):
                over = True

        screen.fill((0, 0, 20))
        for px, py in pellets:
            pygame.draw.circle(screen, (255, 215, 130), (px * CELL + CELL // 2, py * CELL + CELL // 2), 3)
        pygame.draw.circle(screen, (255, 255, 0), (pac[0] * CELL + 10, pac[1] * CELL + 10), 9)
        pygame.draw.circle(screen, (255, 80, 120), (ghost[0] * CELL + 10, ghost[1] * CELL + 10), 9)

        msg = f'Score: {score}'
        if over:
            msg += ' | Game Over (blink to restart)'
        screen.blit(font.render(msg, True, (255, 255, 255)), (10, 8))
        pygame.display.flip()
        clock.tick(9)

    pygame.quit()


if __name__ == '__main__':
    main()
