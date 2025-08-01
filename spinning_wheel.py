import pygame
import math
import random

# Configuraciones
WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2, HEIGHT // 2
RADIUS = 350
SECTORS = 25
ANGLE_PER_SECTOR = 360 / SECTORS
FONT_SIZE = 24

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rueda Giratoria")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Crear superficie de la rueda
wheel_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

for i in range(SECTORS):
    start_angle = math.radians(i * ANGLE_PER_SECTOR)
    end_angle = math.radians((i + 1) * ANGLE_PER_SECTOR)
    color = [random.randint(0, 255) for _ in range(3)]
    points = [CENTER]
    # Dibujar triangulo para cada sector
    for angle in (start_angle, end_angle):
        x = CENTER[0] + RADIUS * math.cos(angle)
        y = CENTER[1] + RADIUS * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(wheel_surface, color, points)
    # Número en el sector
    text = font.render(str(i + 1), True, (0, 0, 0))
    text_angle = (i + 0.5) * ANGLE_PER_SECTOR
    text_x = CENTER[0] + (RADIUS / 2) * math.cos(math.radians(text_angle)) - text.get_width() / 2
    text_y = CENTER[1] + (RADIUS / 2) * math.sin(math.radians(text_angle)) - text.get_height() / 2
    wheel_surface.blit(text, (text_x, text_y))

angle = 0
angular_velocity = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                angular_velocity = random.uniform(10, 15)  # Velocidad inicial aleatoria

    if angular_velocity > 0:
        angle += angular_velocity
        angular_velocity *= 0.99  # Reducir velocidad gradualmente
        if angular_velocity < 0.1:
            angular_velocity = 0

    rotated_wheel = pygame.transform.rotate(wheel_surface, angle)
    rect = rotated_wheel.get_rect(center=CENTER)

    screen.fill((255, 255, 255))
    screen.blit(rotated_wheel, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
