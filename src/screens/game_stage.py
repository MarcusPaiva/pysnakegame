from datetime import datetime, timedelta

import pygame
from pygame import Surface, SurfaceType

from src.GameObjects.player import Player
from src.GameObjects.fruit import Fruit
from src.bounding_box import RectBoundingBox
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
        self._clock = pygame.time.Clock()
        self._running = True
        self._game_bounds = RectBoundingBox(30, 100, self._screen.get_width() - 30, self._screen.get_height() - 30)
        self._game_header_bounds = RectBoundingBox(0, 0, self._screen.get_width(), self._game_bounds.initial_position.y - 25)
        self._player = Player(screen, self._game_bounds)
        self._fruit = Fruit(screen, self._game_bounds)
        self._collision = 0
        self._end_game = False
        pygame.font.init()
        pygame.mixer.init()
        self._main_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', 80)
        self._header_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', 80)
        self._paused_text = self._main_font.render('Paused', False, (255, 255, 255))
        self._points_text = self._main_font.render(f'Points {self._player.points}', False, (255, 255, 255))
        self._last_key_pressed = datetime.now()
        pygame.key.set_repeat(50,200)
        pygame.mixer.music.load(r'./src/assets/sounds/music/main_song.mp3')

    def setup(self) -> None:
        """
        Stage setup.
        """
        self._player.points = 1
        self._fruit.generate()
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.3)

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
        tm = datetime.now() - self._last_key_pressed
        if tm > timedelta(milliseconds=200):
            if self._pause:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self._pause = False
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self._pause = True

    def __in_game(self):
        """
        In game.
        """
        if not self._pause:
            self._player.update()
            self._fruit.update()
        self._fruit.draw()
        self._player.draw()

        if detect_player_fruit_collision(self._player, self._fruit):
            self._fruit.generate()
            self._player.add_point()

        if self_collision(self._player):
            self._collision += 1
            self._pause = True
            self._end_game = True
            print(f"Colidiu! {self._collision}")

    def __pause_menu(self):
        if self._pause:
            self._screen.blit(self._paused_text, (self._screen.get_width() / 2, self._screen.get_height() / 2))


    def loop(self):
        """
        Main game loop.
        """
        while self._running:
            self.__user_io_detection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            self._screen.fill("orange")
            self.__draw_header()
            self.__draw_scenario()
            self.__in_game()
            self.__pause_menu()

            pygame.display.flip()
            self._clock.tick(60)