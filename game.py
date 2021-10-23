import pygame


class Game:
    def __init__(self, surf):
        self.surf = surf

    def draw(self):
        pygame.draw.rect(self.surf, "black", (self.surf.get_rect().w // 2, 0, 2, self.surf.get_rect().h))
