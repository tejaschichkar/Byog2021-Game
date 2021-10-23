import pygame

WIDTH = 700
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")


def redraw_screen():
    WIN.fill("white")
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
