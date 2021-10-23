import pygame
from game import Game

WIDTH = 900
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")

game = Game(WIN, WIDTH, HEIGHT)


def redraw_screen():
    WIN.fill("white")
    game.draw()
    pygame.display.flip()


def main():
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.on_event(event)
        redraw_screen()
        clock.tick(15)
    pygame.quit()


main()
