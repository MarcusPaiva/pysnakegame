from datetime import datetime, timedelta

import pygame
from pygame import Surface, SurfaceType

from src.GameObjects.player import Player
from src.GameObjects.fruit import Fruit
from src.game_components.modal import Modal, Options
from src.game_engines.bounding_box import RectBoundingBox
from src.game_engines.game_brief import GameBrief
from src.game_engines.game_input import Keyboard, Keys
from src.game_engines.game_status import GameStatus
from src.game_engines.screen_game import ScreenGame
from src.screens.game_screens import GameScreen
from src.utils.game_collision import circle_collision_detections


def detect_player_fruit_collision(player:Player, fruit:Fruit) -> bool:
    """
    Player and Fruit collision detection.
    :param player: Players' GameObject.
    :param fruit: Fruit's GameObject.
    :return: Collision status as boolean.
    """
    return circle_collision_detections(player.position, player.radius, fruit.position, fruit.radius)

def self_collision(player:Player) -> bool:
    """
    Self player collision detection.
    :param player: Players' GameObject.
    :return: Collision status as boolean.
    """
    last = player.position
    if len(player.positions) > 1:
        for idx, pos in enumerate(player.positions[:-1]):
            return circle_collision_detections(pos, player.radius, last, player.radius)


class Stage(GameScreen):
    def __init__(self, screen:Surface | SurfaceType):
        self._screen = screen
        self._pause = False
        self._game_bounds = RectBoundingBox(30, 100, self._screen.get_width() - 30, self._screen.get_height() - 30)
        self._game_header_bounds = RectBoundingBox(0, 0, self._screen.get_width(), self._game_bounds.initial_position.y - 25)
        self._player = Player(screen, self._game_bounds)
        self._fruit = Fruit(screen, self._game_bounds)
        self._modal_game_over = Modal(self._screen, 250, 150, "Game Over")
        self._modal_pause = Modal(self._screen, 250, 150, "Paused")
        self._collision = 0
        self._end_game = False
        pygame.font.init()
        pygame.mixer.init()
        self._main_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', 80)
        self._header_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', 80)
        self._paused_text = self._main_font.render('Paused', False, (255, 255, 255))
        self._points_text = self._main_font.render(f'Points {self._player.points}', False, (255, 255, 255))
        self._last_key_pressed = []
        self._game_brief = GameBrief()
        self._game_status = GameStatus()
        pygame.key.set_repeat(50,200)
        pygame.mixer.music.load(r'./src/assets/sounds/music/main_song.mp3')
        self._game_keyboard = Keyboard()

    def reset(self):
        self._collision = 0
        self._player = Player(self._screen, self._game_bounds)
        self._fruit.generate()
        self._end_game = False
        self._pause = False

    def __continue_option(self):
        """
        Continue event.
        :return:
        """
        self._pause = False

    def __try_again_option(self):
        self.reset()

    def setup(self) -> None:
        """
        Stage setup.
        """
        self._player.points = 1
        self._fruit.generate()
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.3)
        self._modal_game_over.setup()
        self._modal_game_over.show(False)
        self.__setup_modal_game_over_options()
        self._modal_pause.setup()
        self._modal_pause.show(False)
        self.__setup_modal_pause_options()

    def __main_menu_option(self):
        self._player = Player(self._screen, self._game_bounds)
        self._fruit = Fruit(self._screen, self._game_bounds)
        self._game_status.current_screen = ScreenGame.main_menu

    def __setup_modal_game_over_options(self):
        options = [
            Options("Try again", self.__try_again_option, "green", "white"),
            Options("Main Menu", self.__main_menu_option, "red", "white"),
        ]
        self._modal_game_over.add_options(options)

    def __setup_modal_pause_options(self):
        options = [
            Options("Continue", self.__continue_option, "green", "white"),
            Options("Main Menu", self.__main_menu_option, "red", "white"),
        ]
        self._modal_pause.add_options(options)

    def __draw_score(self):
        """
        Draw score on header.
        :return:
        """
        self._points_text = self._main_font.render(f'Points {self._player.points}', False, (255, 255, 255))
        self._screen.blit(
            self._points_text,
            (self._game_header_bounds.initial_position.x + 10, self._game_header_bounds.initial_position.y)
        )

    def __draw_header(self):
        """
        Draw header.
        """
        pygame.draw.rect(
            self._screen,
            "#596869", [
                self._game_header_bounds.initial_position.x,
                self._game_header_bounds.initial_position.y,
                self._game_header_bounds.size.x,
                self._game_header_bounds.size.y
            ],
            0,
        )
        self.__draw_score()

    def __draw_scenario(self):
        """
        Draw scenario.
        """
        pygame.draw.rect(
            self._screen,
            "#A41623", [
                0,
                self._game_bounds.initial_position.y - 25,
                self._screen.get_width(),
                self._screen.get_height()
            ],
            0,
        )
        pygame.draw.rect(
            self._screen,
            "black", [
                self._game_bounds.initial_position.x-2,
                self._game_bounds.initial_position.y-2,
                self._game_bounds.size.x + 4,
                self._game_bounds.size.y + 4
            ],
            0,
        )
        pygame.draw.rect(
            self._screen,
            "orange", [
                self._game_bounds.initial_position.x,
                self._game_bounds.initial_position.y,
                self._game_bounds.size.x,
                self._game_bounds.size.y
            ],
            0 ,
        )

    def __user_io_detection(self):
        """
        Main user detection action.
        :return:
        """
        pause_detection = True
        if self._game_keyboard.user_is_pressing:
            keys = self._game_keyboard.current_keys_pressing
            if not self._pause and Keys.escape not in self._last_key_pressed and pause_detection:
                if Keys.escape in keys:
                    self._pause = True
                    pause_detection = False
            if self._pause and Keys.escape not in self._last_key_pressed and pause_detection:
                if Keys.escape in keys:
                    self._pause = False
            self._last_key_pressed = keys
        else:
            self._last_key_pressed = []

    def __in_game(self):
        """
        In game.
        """
        if not self._pause and not self._end_game:
            self._player.update()
            self._fruit.update()
        self._fruit.draw()
        self._player.draw()

        if detect_player_fruit_collision(self._player, self._fruit):
            self._fruit.generate()
            self._player.add_point()

        if self_collision(self._player) and not self._end_game:
            self._game_brief.add_global_points( self._player.points )
            self._game_brief.increment_tries()
            self._collision += 1
            self._pause = True
            self._end_game = True
            print(f"Colidiu! {self._collision}")

    def __pause_menu(self):
        self._modal_pause.show(self._pause)
        self._modal_pause.update()
        self._modal_pause.draw()

    def __game_over_menu(self):
        self._modal_game_over.show(self._end_game)
        self._modal_game_over.update()
        self._modal_game_over.draw()


    def loop(self):
        """
        Main game loop.
        """
        self._game_keyboard.detect_buttons()
        self._screen.fill("orange")
        self.__user_io_detection()
        self.__draw_header()
        self.__draw_scenario()
        self.__in_game()
        self.__pause_menu()
        self.__game_over_menu()