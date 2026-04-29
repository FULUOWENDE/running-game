import pygame

from src.constants import FPS, HEIGHT, TITLE, WIDTH
from src.game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    game = Game(screen)
    game.run()
    game.cleanup()
    pygame.quit()


if __name__ == "__main__":
    main()
