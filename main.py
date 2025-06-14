import pygame

from src.GameManagement import GameManagement
from src.screens.SplashScreen import SplashScreen
# from src.screens.game_stage import Stage
# from src.screens.main_menu import MainMenu

pygame.init()
screen = pygame.display.set_mode((1100, 720))
pygame.display.set_caption("PySnake Game")

splash = SplashScreen(screen)
splash.setup()
splash.loop()

game_management = GameManagement(screen)
game_management.setup()
game_management.loop()

# main_menu = MainMenu(screen)
# main_menu.setup()
# main_menu.loop()

# stage = Stage(screen)
# stage.setup()
# stage.loop()

pygame.quit()