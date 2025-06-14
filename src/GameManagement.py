import pygame
from pygame import Surface, SurfaceType

from src.screen_game import ScreenGame
from src.screens.game_stage import Stage
from src.screens.main_menu import MainMenu


class GameManagement:
    def __init__(self, screen: Surface | SurfaceType):
        self._main_menu = MainMenu(screen, self)
        self._game_stage = Stage(screen)
        self._running = True
        self._clock = pygame.time.Clock()
        self._current_screen = ScreenGame.main_menu

    def setup(self):
        self._main_menu.setup()
        self._game_stage.setup()

    def current_screen(self) -> ScreenGame:
        return self._current_screen

    def set_current_screen(self, current_screen:ScreenGame):
        self._current_screen = current_screen

    def _process_screen(self):
        if self._current_screen == ScreenGame.main_menu:
            self._main_menu.loop()
        else:
            self._game_stage.loop()

    def exit_game(self):
        self._running = False

    def loop(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
            self._process_screen()
            pygame.display.flip()
            self._clock.tick(60)