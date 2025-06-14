import pygame
from pygame import Surface, SurfaceType

from src.game_components.button import Button
from src.game_engines.game_status import GameStatus
from src.game_engines.screen_game import ScreenGame


class MainMenu:
    def __init__(self, screen: Surface | SurfaceType):
        self._screen = screen
        self._main_font = None
        self._main_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', 120)
        self._start_game_btn = Button(screen, 400, 400, "Start Game",on_click=self.__go_to_game)
        self._exit_game_game_btn = Button(screen, 500, 500, "Exit",on_click=self.__exit_game)
        self._game_status = GameStatus()

    def __go_to_game(self):
        self._game_status.current_screen = ScreenGame.game_stage

    def __exit_game(self):
        self._game_status.close_game()

    def setup(self):
        self._start_game_btn.hover_color("#596869")
        self._start_game_btn.setup()
        self._exit_game_game_btn.hover_color("red")
        self._exit_game_game_btn.setup()

    def _process(self):
        self._start_game_btn.update()
        self._exit_game_game_btn.update()

    def _draw(self):
        self._start_game_btn.draw()
        self._exit_game_game_btn.draw()

    def loop(self):
        self._screen.fill("orange")
        self._process()
        self._draw()
