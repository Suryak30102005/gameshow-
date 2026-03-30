from __future__ import annotations

import pygame

from Games.common import event_recent, read_event

W, H = 800, 420


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('FacePlay - Super Mario')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    player = pygame.Rect(80, H - 90, 36, 56)
    vx = 0
    vy = 0.0
    on_ground = True
    paused = False
    obstacles = [pygame.Rect(500, H - 60, 30, 30), pygame.Rect(760, H - 80, 50, 50)]
    score = 0

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        payload = read_event()
        ge = payload.get('event', {}) if event_recent(payload) else {}

        if ge.get('pause') or ge.get('left_wink'):
            paused = not paused
        if ge.get('resume'):
            paused = False

        if paused:
            screen.fill((15, 15, 35))
            screen.blit(font.render('Paused (left wink/p to toggle)', True, (255, 255, 255)), (220, 180))
            pygame.display.flip()
            clock.tick(30)
            continue

        head = ge.get('head', 'CENTER')
        vx = -4 if head == 'LEFT' else 4 if head == 'RIGHT' else 0
        if ge.get('blink'):
            vx *= 2

        jump = ge.get('eyebrow_raise') or head in ('UP',)
        if jump and on_ground:
            vy = -10.5
            on_ground = False

        vy += 0.42
        player.x += vx
        player.y += int(vy)

        floor = H - 34
        if player.bottom >= floor:
            player.bottom = floor
            vy = 0
            on_ground = True

        for ob in obstacles:
            ob.x -= 4
            if ob.right < 0:
                ob.left = W + 180
                score += 1
            if player.colliderect(ob):
                score = 0
                player.x, player.y = 80, H - 90
                vy = 0

        screen.fill((90, 190, 255))
        pygame.draw.rect(screen, (80, 60, 30), (0, floor, W, H - floor))
        pygame.draw.rect(screen, (255, 60, 60), player)
        for ob in obstacles:
            pygame.draw.rect(screen, (20, 130, 20), ob)
        screen.blit(font.render(f'Score: {score}', True, (0, 0, 0)), (10, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
