import pygame
import os
import random


class Enemy:
    def __init__(self, surf):
        self.surf = surf
        self.running_images = []
        self.standing_images = []
        self.moving = False
        self.standing = True
        for i in range(1, 6):
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

    def draw(self):
        y = 100 if self.lane == "left" else 300
        if self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.standing_image_index]
        elif self.moving:
            pass
        self.surf.blit(self.image, (200, y))


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
        self.running_image_index = 0
        self.standing_image_index = 0
        self.image = self.standing_images[self.standing_image_index]
        self.moving = False
        self.standing = True

    def draw(self, x):
        if self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.standing_image_index]
        elif self.moving:
            self.running_image_index = (self.running_image_index + 1) % len(self.running_images)
            self.image = self.running_images[self.running_image_index]
        if self.direction == "left":
            self.surf.blit(self.image, (x, 100))
        else:
            self.surf.blit(self.image, (x, 300))


class Game:
    def __init__(self, surf, win_width, win_height):
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
        self.enemy = Enemy(self.surf)

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
        if self.lane == "right":
            pygame.draw.rect(self.surf, "green",
                             (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)
        elif self.lane == "left":
            pygame.draw.rect(self.surf, "green", (0, 0, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)
        self.enemy.draw()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
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
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.pressed_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.pressed_right = False
