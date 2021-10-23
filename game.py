import pygame
import os
import random


def check_collision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


class Bullet:
    def __init__(self, surf):
        self.surf = surf
        self.images = []
        for i in range(1, 3):
            self.images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "bullet", f"scifi_blasterfire_{i}.png")), (28, 5)))
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.x = 0
        self.drawn_once = False
        self.mask = pygame.mask.from_surface(self.image)
        self.y = 0

    def draw(self, x, y):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.surf.blit(self.image, (x, y))


class Enemy:
    def __init__(self, surf):
        self.surf = surf
        self.running_images = []
        self.standing_images = []
        self.moving = True
        self.standing = False
        for i in range(1, 6):
            self.running_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "running", f"scifi_alien_run_{i}.png")), (200, 100)))
            self.running_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "running", f"scifi_alien_run_{i}.png")), (200, 100)))
        for i in range(1, 3):
            self.standing_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "standing", f"scifi_alien_idle_{i}.png")), (200, 100)))
        self.lane = random.choice(["left", "right"])
        self.running_image_index = 0
        self.standing_image_index = 0
        self.image = self.standing_images[self.standing_image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.surf.get_rect().w
        self.y = 150 if self.lane == "left" else 350

    def draw(self):
        if self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.standing_image_index]
        elif self.moving:
            self.running_image_index = (self.running_image_index + 1) % len(self.running_images)
            self.image = self.running_images[self.running_image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.surf.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= 5


class Player:
    def __init__(self, surf, direction):
        self.surf = surf
        self.direction = direction
        self.running_images = []
        self.standing_images = []
        for i in range(1, 7):
            self.running_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "running", direction, f"scifi_marine_run_{i}.png")), (150, 150)))
        for i in range(1, 3):
            self.standing_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "standing", direction, f"scifi_marine_stand_{i}.png")),
                    (150, 150)))
            self.standing_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "standing", direction, f"scifi_marine_stand_{i}.png")),
                    (150, 150)))
        self.running_image_index = 0
        self.standing_image_index = 0
        self.image = self.standing_images[self.standing_image_index]
        self.moving = False
        self.standing = True
        self.bullets = []

    def draw(self, x):
        y = 100 if self.direction == "left" else 300
        if self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.standing_image_index]
        elif self.moving:
            self.running_image_index = (self.running_image_index + 1) % len(self.running_images)
            self.image = self.running_images[self.running_image_index]
        self.surf.blit(self.image, (x, y))
        bullet_copy = self.bullets
        for bullet in self.bullets:
            if bullet.x > self.surf.get_rect().w:
                bullet_copy.remove(bullet)
                continue
            if bullet.drawn_once:
                bullet.x += 20
                bullet.draw(bullet.x, y + 90)
            else:
                bullet.draw(x + 105, y + 90)
                bullet.drawn_once = True
        self.bullets = bullet_copy

    def shoot(self):
        bullet = Bullet(self.surf)
        self.bullets.append(bullet)


class Game:
    def __init__(self, surf, win_width, win_height, add_enemy_event):
        self.surf = surf
        self.bg_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), (win_width, win_height))
        self.win_width = win_width
        self.win_height = win_height
        self.player_x = 20
        self.left_player = Player(self.surf, "left")
        self.right_player = Player(self.surf, "right")
        self.player_width = self.left_player.image.get_rect().w
        self.player_height = self.left_player.image.get_rect().h
        self.player_speed = 10
        self.pressed_left = False
        self.pressed_right = False
        self.lane = "right"
        self.enemies = []
        self.add_enemy_event = add_enemy_event
        self.added_first_enemy = False

    def draw(self):
        if self.pressed_left:
            self.player_x -= self.player_speed
        elif self.pressed_right:
            self.player_x += self.player_speed
        if self.player_x < 0:
            self.player_x = 0
            if self.left_player.moving:
                self.left_player.moving = False
                self.left_player.standing = True
                self.right_player.moving = False
                self.right_player.standing = True
        if self.player_x > self.win_width - self.player_width:
            self.player_x = self.win_width - self.player_width
            if self.left_player.moving:
                self.left_player.moving = False
                self.left_player.standing = True
                self.right_player.moving = False
                self.right_player.standing = True
        self.surf.blit(self.bg_img, (0, 0))
        pygame.draw.rect(self.surf, "white", (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, 3))
        self.left_player.draw(self.player_x)
        self.right_player.draw(self.player_x)
        for enemy in self.enemies:
            enemy.move()
            enemy.draw()

        if self.lane == "right":
            pygame.draw.rect(self.surf, "green",
                             (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)
        elif self.lane == "left":
            pygame.draw.rect(self.surf, "green", (0, 0, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)
        temp_bullets = self.left_player.bullets
        temp_enemies = self.enemies
        for bullet in self.left_player.bullets:
            for enemy in self.enemies:
                if check_collision(enemy, bullet):
                    temp_bullets.remove(bullet)
                    temp_enemies.remove(enemy)
        self.left_player.bullets = temp_bullets
        self.enemies = temp_enemies
        temp_bullets = self.right_player.bullets
        temp_enemies = self.enemies
        for bullet in self.right_player.bullets:
            for enemy in self.enemies:
                if check_collision(enemy, bullet):
                    temp_bullets.remove(bullet)
                    temp_enemies.remove(enemy)
        self.right_player.bullets = temp_bullets
        self.enemies = temp_enemies

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.lane == "left":
                    self.left_player.shoot()
                else:
                    self.right_player.shoot()
            elif event.key == pygame.K_UP:
                self.lane = "left" if self.lane == "right" else "right"
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                self.left_player.moving = True
                self.left_player.standing = False
                self.right_player.moving = True
                self.right_player.standing = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.pressed_left = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.pressed_right = True
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                self.left_player.moving = False
                self.left_player.standing = True
                self.right_player.moving = False
                self.right_player.standing = True
                self.pressed_left = False
                self.pressed_right = False
        elif event.type == self.add_enemy_event:
            if not self.added_first_enemy:
                self.added_first_enemy = True
                pygame.time.set_timer(self.add_enemy_event, 3500)
            self.enemies.append(Enemy(self.surf))
