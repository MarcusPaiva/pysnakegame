import pygame
from pygame import Surface, SurfaceType

from src.game_engines.game_status import GameStatus
from src.game_engines.screen_game import ScreenGame
from src.screens.game_stage import Stage
from src.screens.main_menu import MainMenu


class GameManagement:
    def __init__(self, screen: Surface | SurfaceType):
        """
        Game Management initializer.
        :param screen: Game window.
        """
        self._main_menu = MainMenu(screen)
        self._game_stage = Stage(screen)
        self._clock = pygame.time.Clock()
        self._current_screen = ScreenGame.main_menu
        self._game_status = GameStatus()

    def setup(self):
        """
        Setup event.
        """
        self._main_menu.setup()
        self._game_stage.setup()

    @property
    def current_screen(self) -> ScreenGame:
        """
        Get current screen.
        :return: Current screen
        """
        return self._game_status.current_screen

    # def set_current_screen(self, current_screen:ScreenGame):
    #     """
    #     Set current screen, this make game change screen.
    #     :param current_screen: Current screen enum.
    #     """
    #     self._current_screen = current_screen

    def _process_screen(self):
        """
        Process screen event.
        :return:
        """
        if self.current_screen == ScreenGame.main_menu:
            self._main_menu.loop()
        else:
            self._game_stage.loop()

    def exit_game(self):
        """
        Exit game.
        """
        self._game_status.close_game()

    def loop(self):
        """
        Main game loop.
        """
        while self._game_status.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
            self._process_screen()
            pygame.display.flip()
            self._clock.tick(60)