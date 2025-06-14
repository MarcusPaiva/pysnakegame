import pygame

from src.screens.SplashScreen import SplashScreen
from src.screens.game_stage import Stage

pygame.init()
screen = pygame.display.set_mode((1100, 720))
pygame.display.set_caption("PySnake Game")

splash = SplashScreen(screen)
splash.setup()
splash.loop()

stage = Stage(screen)
stage.setup()
stage.loop()

pygame.quit()