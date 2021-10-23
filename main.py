import pygame
from game import Game

pygame.init()

WIDTH = 900
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")


def redraw_screen():
    WIN.fill("white")
    game.draw()
    pygame.display.flip()


def main():
    global game

    running = True
    clock = pygame.time.Clock()
    ADD_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 1500, 1)
    game = Game(WIN, WIDTH, HEIGHT, ADD_ENEMY)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.on_event(event)
        redraw_screen()
        clock.tick(15)
    pygame.quit()


main()
