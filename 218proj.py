import pygame
import random

# Initialize the game engine
pygame.init()

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Space Invaders")

# Frame rate manager
fps_clock = pygame.time.Clock()

# Define the player's ship
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.move_speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.move_speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.move_speed

    def fire_bullet(self):
        new_bullet = PlayerBullet(self.rect.centerx, self.rect.top)
        all_sprites.add(new_bullet)
        player_bullets.add(new_bullet)

# Define enemy ships with simple behavior
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed = 3
        self.behavior = "Idle"

    def update(self):
        if self.behavior == "Idle":
            if random.random() < 0.01:
                self.behavior = "Moving"
        elif self.behavior == "Moving":
            self.rect.x += self.move_speed
            if self.rect.right >= WIDTH or self.rect.left <= 0:
                self.move_speed *= -1
            if random.random() < 0.02:
                self.behavior = "Shooting"
        elif self.behavior == "Shooting":
            if random.random() < 0.05:
                new_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, -5)
                all_sprites.add(new_bullet)
                enemy_bullets.add(new_bullet)
            self.behavior = "Moving"

# Define bullets for both player and enemies
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocity = velocity

    def update(self):
        self.rect.y -= self.velocity
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Separate classes for player and enemy bullets
class PlayerBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, 5)

class EnemyBullet(Bullet):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, velocity)

# Create groups for sprites
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Initialize player ship
player = PlayerShip()
all_sprites.add(player)

# Initialize enemy ships
for i in range(5):
    enemy = EnemyShip(100 * i + 50, 50)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire_bullet()

    # Update game objects
    all_sprites.update()

    # Detect collisions
    for bullet in player_bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)
        if hits:
            bullet.kill()

    if pygame.sprite.spritecollideany(player, enemy_bullets):
        running = False

    # Render the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    fps_clock.tick(60)

pygame.quit()
