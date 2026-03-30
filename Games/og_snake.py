from __future__ import annotations

import random

import pygame

from Games.common import event_recent, read_event

W = H = 520
CELL = 20


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('FacePlay - OG Snake')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    snake = [(12, 12), (11, 12), (10, 12)]
    direction = (1, 0)
    food = (random.randint(0, 25), random.randint(0, 25))
    score = 0

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        payload = read_event()
        ge = payload.get('event', {}) if event_recent(payload) else {}

        head = ge.get('head', 'CENTER')
        if head == 'LEFT' and direction != (1, 0):
            direction = (-1, 0)
        elif head == 'RIGHT' and direction != (-1, 0):
            direction = (1, 0)
        elif head == 'UP' and direction != (0, 1):
            direction = (0, -1)
        elif head == 'DOWN' and direction != (0, -1):
            direction = (0, 1)

        speed = 10
        if ge.get('blink'):
            speed = 16
        if ge.get('eyebrow_raise'):
            speed = 5

        hx, hy = snake[0]
        nx, ny = hx + direction[0], hy + direction[1]
        if nx < 0 or ny < 0 or nx >= W // CELL or ny >= H // CELL or (nx, ny) in snake:
            snake = [(12, 12), (11, 12), (10, 12)]
            direction = (1, 0)
            score = 0
        else:
            snake.insert(0, (nx, ny))
            if (nx, ny) == food:
                score += 1
                food = (random.randint(0, 25), random.randint(0, 25))
            else:
                snake.pop()

        screen.fill((15, 15, 20))
        for sx, sy in snake:
            pygame.draw.rect(screen, (60, 220, 60), (sx * CELL, sy * CELL, CELL - 1, CELL - 1))
        pygame.draw.rect(screen, (255, 80, 80), (food[0] * CELL, food[1] * CELL, CELL - 1, CELL - 1))
        screen.blit(font.render(f'Score: {score}', True, (255, 255, 255)), (10, 10))
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


if __name__ == '__main__':
    main()
