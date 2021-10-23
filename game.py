import pygame


class Game:
    def __init__(self, surf):
        self.surf = surf
        self.bg_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), (700, 600))

    def draw(self):
        self.surf.blit(self.bg_img, (0, 0))
        pygame.draw.rect(self.surf, "white", (self.surf.get_rect().w // 2, 0, 3, self.surf.get_rect().h))
