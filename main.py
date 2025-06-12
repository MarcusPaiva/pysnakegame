import pygame

from src.SplashScreen import SplashScreen
from src.game_stage import Stage

pygame.init()
screen = pygame.display.set_mode((1280, 720))

splash = SplashScreen(screen)
splash.show()

stage = Stage(screen)
stage.setup()
stage.loop()

pygame.quit()