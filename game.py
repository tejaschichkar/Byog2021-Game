import pygame


class Game:
    def __init__(self, surf, win_width, win_height):
        self.surf = surf
        self.bg_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), (win_width, win_height))
        self.win_width = win_width
        self.win_height = win_height
        self.player_x = 20
        self.left_player = pygame.Rect(self.player_x, 50, 50, 50)
        self.player_width = 50
        self.player_height = 50
        self.speed = 4
        self.pressed_left = False
        self.pressed_right = False

    def draw(self):
        if self.pressed_left:
            self.player_x -= self.speed
        elif self.pressed_right:
            self.player_x += self.speed
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > self.win_width - self.player_width:
            self.player_x = self.win_width - self.player_width
        self.left_player = pygame.Rect(self.player_x, 50, 50, 50)
        self.surf.blit(self.bg_img, (0, 0))
        pygame.draw.rect(self.surf, "white", (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, 3))
        pygame.draw.rect(self.surf, "white", self.left_player)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.pressed_left = True
            elif event.key == pygame.K_RIGHT:
                self.pressed_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.pressed_left = False
            elif event.key == pygame.K_RIGHT:
                self.pressed_right = False
