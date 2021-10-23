import pygame
from game import Game

WIDTH = 700
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")

game = Game(WIN)


def redraw_screen():
    WIN.fill("white")
    game.draw()
    pygame.display.flip()


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        redraw_screen()
    pygame.quit()


main()
