import pygame

from src.game_management import GameManagement
from src.screens.SplashScreen import SplashScreen

# Pygame initializer window.
pygame.init()
screen = pygame.display.set_mode((1100, 720))
pygame.display.set_caption("PySnake Game")

# Splash screen
splash = SplashScreen(screen)
splash.setup()
splash.loop()

# Game Management
game_management = GameManagement(screen)
game_management.setup()
game_management.loop()

pygame.quit()