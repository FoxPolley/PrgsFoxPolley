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

HUMAN_HEIGHT = (RADIUS * 2) // 5  # tamaño de los humanos

class Human:
    def __init__(self, x, base_y):
        self.x = x
        self.base_y = base_y
        self.color = [random.randint(0, 255) for _ in range(3)]
        self.jump_phase = random.random() * math.tau
        self.arm_up = False
        self.timer = 0

    def update(self, spinning):
        if spinning:
            self.jump_phase += 0.2
        else:
            self.timer += 0.15
            if self.timer > 0.3:
                self.arm_up = not self.arm_up
                self.timer = 0

    def draw(self, surface, spinning):
        h = HUMAN_HEIGHT
        offset = -abs(math.sin(self.jump_phase)) * h * 0.3 if spinning else 0
        y = self.base_y + offset

        # Cabeza
        pygame.draw.circle(surface, self.color, (self.x, int(y - h)), int(h * 0.15))
        # Cuerpo
        pygame.draw.line(surface, self.color, (self.x, y - h * 0.85), (self.x, y - h * 0.4), 4)

        # Brazos
        if spinning:
            pygame.draw.line(surface, self.color, (self.x, y - h * 0.75), (self.x - h * 0.3, y - h * 0.9), 4)
            pygame.draw.line(surface, self.color, (self.x, y - h * 0.75), (self.x + h * 0.3, y - h * 0.9), 4)
        else:
            if self.arm_up:
                pygame.draw.line(surface, self.color, (self.x, y - h * 0.75), (self.x - h * 0.2, y - h * 0.95), 4)
                pygame.draw.line(surface, self.color, (self.x, y - h * 0.75), (self.x + h * 0.2, y - h * 0.95), 4)
            else:
                pygame.draw.line(surface, self.color, (self.x, y - h * 0.75), (self.x - h * 0.2, y - h * 0.55), 4)
                pygame.draw.line(surface, self.color, (self.x, y - h * 0.75), (self.x + h * 0.2, y - h * 0.55), 4)

        # Piernas
        pygame.draw.line(surface, self.color, (self.x, y - h * 0.4), (self.x - h * 0.25, y), 4)
        pygame.draw.line(surface, self.color, (self.x, y - h * 0.4), (self.x + h * 0.25, y), 4)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rueda Giratoria")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Crear superficie de la rueda
wheel_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Crear humanos
humans = []
spacing = WIDTH // 11
base_y = HEIGHT - 20
for i in range(10):
    x = spacing * (i + 1)
    humans.append(Human(x, base_y))

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

    for human in humans:
        human.update(angular_velocity > 0)

    rotated_wheel = pygame.transform.rotate(wheel_surface, angle)
    rect = rotated_wheel.get_rect(center=CENTER)

    screen.fill((255, 255, 255))
    screen.blit(rotated_wheel, rect)
    for human in humans:
        human.draw(screen, angular_velocity > 0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
