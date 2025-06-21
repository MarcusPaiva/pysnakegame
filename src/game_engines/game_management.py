from datetime import datetime, timedelta

import pygame
from pygame import Surface, SurfaceType

from src.game_engines.game_brief import GameBrief
from src.game_engines.game_status import GameStatus
from src.game_engines.screen_game import ScreenGame
from src.screens.game_stage import Stage
from src.screens.main_menu import MainMenu
from src.utils.game_storage import GameBriefStorage


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
        self._game_brief = GameBrief()
        self._last_save = datetime.now()
        self._game_storage = GameBriefStorage()

    def setup(self):
        """
        Setup event.
        """
        self._main_menu.setup()
        self._game_stage.setup()
        self._game_storage.load_brief()

    @property
    def current_screen(self) -> ScreenGame:
        """
        Get current screen.
        :return: Current screen
        """
        return self._game_status.current_screen

    def _process_screen(self):
        """
        Process screen event.
        :return:
        """
        if self._game_status.change_screen_trigger:
            self._game_stage.reset()
            self._game_status.dismiss_change_screen_trigger()
        if self.current_screen == ScreenGame.main_menu:
            self._main_menu.loop()
        else:
            self._game_stage.loop()

    def save_event(self):
        """
        Save brief event.
        """
        tm = datetime.now() - self._last_save
        if tm > timedelta(milliseconds=1000):
            self._game_storage.save_brief()
            self._last_save = datetime.now()

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
            self.save_event()
            self._process_screen()
            pygame.display.flip()
            self._clock.tick(60)