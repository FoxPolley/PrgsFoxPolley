import math
import random
import pygame
from pygame import gfxdraw

WIDTH, HEIGHT = 600, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250
NUM_SECTORS = 8
ANGLE_PER_SECTOR = 360 / NUM_SECTORS
FRICTION = 0.1

# Colors for sectors
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (200, 100, 50),
    (150, 0, 150),
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Pre-render wheel surface
wheel_surface = pygame.Surface((RADIUS * 2, RADIUS * 2), pygame.SRCALPHA)
for i in range(NUM_SECTORS):
    center_deg = 90 - i * ANGLE_PER_SECTOR
    start = center_deg - ANGLE_PER_SECTOR / 2
    end = center_deg + ANGLE_PER_SECTOR / 2
    gfxdraw.pie(wheel_surface, RADIUS, RADIUS, RADIUS, int(start), int(end), COLORS[i])
    angle_rad = math.radians(center_deg)
    text = font.render(str(i + 1), True, (0, 0, 0))
    text_pos = (
        RADIUS + int(math.cos(angle_rad) * RADIUS * 0.6) - text.get_width() // 2,
        RADIUS - int(math.sin(angle_rad) * RADIUS * 0.6) - text.get_height() // 2,
    )
    wheel_surface.blit(text, text_pos)

angle = 0
angular_velocity = 0
active_sector = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and angular_velocity == 0:
            angular_velocity = random.uniform(10, 20)
            active_sector = None

    if angular_velocity > 0:
        angle = (angle + angular_velocity) % 360
        angular_velocity = max(0, angular_velocity - FRICTION)
        if angular_velocity == 0:
            active_sector = int((-angle % 360) / ANGLE_PER_SECTOR)

    rotated = pygame.transform.rotozoom(wheel_surface, -angle, 1)
    rect = rotated.get_rect(center=CENTER)

    screen.fill((255, 255, 255))
    screen.blit(rotated, rect)

    # Draw fixed pointer at top
    pointer = [
        (WIDTH // 2, 20),
        (WIDTH // 2 - 20, 60),
        (WIDTH // 2 + 20, 60),
    ]
    pygame.draw.polygon(screen, (0, 0, 0), pointer)

    if angular_velocity == 0 and active_sector is not None:
        text = font.render(f"Ganador: {active_sector + 1}", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT - 40)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
