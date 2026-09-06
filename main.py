import pygame

from game_engine.game_management import GameManagement
from game_engine.screen import SurfaceScreen
from game_src.screens.SplashScreen import SplashScreen

# Pygame initializer window.
pygame.init()
screen = SurfaceScreen(1100, 720, "PySnake Game")

# Splash screen
splash = SplashScreen(screen)
splash.setup()
splash.loop()

# Game Management
game_management = GameManagement(screen)
game_management.setup()
game_management.loop()

pygame.quit()
