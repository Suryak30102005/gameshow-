from __future__ import annotations

import random

import pygame

from Games.common import event_recent, read_event

W, H = 480, 640


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('FacePlay - Flappy Bird')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 34)

    y, vel = H // 2, 0.0
    pipes = [(W + 120, random.randint(170, H - 170))]
    score = 0
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        event = read_event()
        ge = event.get('event', {}) if event_recent(event) else {}

        flap = ge.get('blink') or ge.get('eyebrow_raise')
        if flap:
            vel = -6.8

        vel += 0.36
        y += vel

        px, gap_y = pipes[-1]
        if px < W - 190:
            pipes.append((W + 80, random.randint(170, H - 170)))
        pipes = [(x - 3, gy) for x, gy in pipes if x > -80]

        bird = pygame.Rect(80, int(y), 30, 30)
        dead = y < 0 or y > H - 30

        for x, gy in pipes:
            top = pygame.Rect(x, 0, 60, gy - 90)
            bot = pygame.Rect(x, gy + 90, 60, H - gy - 90)
            if bird.colliderect(top) or bird.colliderect(bot):
                dead = True
            if x == 80:
                score += 1

        if dead:
            y, vel, score = H // 2, 0.0, 0
            pipes = [(W + 120, random.randint(170, H - 170))]

        screen.fill((120, 200, 255))
        pygame.draw.rect(screen, (255, 230, 0), bird)
        for x, gy in pipes:
            pygame.draw.rect(screen, (30, 160, 30), (x, 0, 60, gy - 90))
            pygame.draw.rect(screen, (30, 160, 30), (x, gy + 90, 60, H - gy - 90))

        screen.blit(font.render(f'Score: {score}', True, (0, 0, 0)), (10, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
