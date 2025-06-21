from datetime import datetime, timedelta
from typing import List

import pygame
from pygame import SurfaceType, Surface
from pygame.rect import RectType, Rect

from src.GameObjects.GameObject import GameObject
from src.game_engines.bounding_box import BoundingBox
from src.game_engines.game_input import Keyboard, Keys


class Player(GameObject):
    def __init__(self, screen:Surface | SurfaceType, game_bounds:BoundingBox):
        self._screen = screen
        self._bounds = game_bounds
        self._player_pos = pygame.Vector2(self._bounds.final_position.x / 2, self._bounds.final_position.y / 2)
        self._speed = 3
        self._last_position = pygame.K_w
        self._radius = 10
        self._sprite = None
        self._point = 1
        self._prev_points = [self._player_pos]
        self._eat_effect = pygame.mixer.Sound(r'./src/assets/sounds/effects/eating.mp3')
        self._eat_effect.set_volume(0.7)
        self._prev_time = datetime.now()
        self._game_keyboard = Keyboard()

    @property
    def points(self):
        return self._point

    def add_point(self):
        pygame.mixer.init()  # Initialize the mixer module.
        self._eat_effect.play(0)
        self._point += 1
        self._speed += self._speed * (self._point / 1000)

    @points.setter
    def points(self, point:int):
        self._point = point


    @property
    def position(self) -> pygame.Vector2:
        return self._player_pos

    @property
    def positions(self) -> List[pygame.Vector2]:
        return self._prev_points

    @property
    def radius(self):
        return self._radius

    @property
    def sprite(self) -> Rect | RectType | None:
        return self._sprite

    def __control_event(self):
        self._game_keyboard.detect_buttons()
        keys = self._game_keyboard.current_keys_pressing
        if Keys.key_up in keys and not self._last_position == pygame.K_w:
            self._last_position = pygame.K_w
        if Keys.key_down in keys and not self._last_position == pygame.K_s:
            self._last_position = pygame.K_s
        if Keys.key_left in keys and not self._last_position == pygame.K_a:
            self._last_position = pygame.K_a
        if Keys.key_right in keys and not self._last_position == pygame.K_d:
            self._last_position = pygame.K_d

    def __move(self):
        # Why does this code create mental knots?
        if self._last_position == pygame.K_w:
            self._player_pos.y -= self._radius * 2 + 3
            if self._player_pos.y - self._radius < self._bounds.initial_position.y:
                self._player_pos.y = self._bounds.final_position.y - self._radius
        if self._last_position == pygame.K_s:
            self._player_pos.y += self._radius * 2 + 3
            if self._player_pos.y + self._radius > self._bounds.final_position.y:
                self._player_pos.y = self._bounds.initial_position.y + (self._radius * 2)
        if self._last_position == pygame.K_a:
            self._player_pos.x -= self._radius * 2 + 3
            if self._player_pos.x - self._radius < self._bounds.initial_position.x:
                self._player_pos.x = self._bounds.final_position.x - self._radius
        if self._last_position == pygame.K_d:
            self._player_pos.x += self._radius * 2 + 3
            if self._player_pos.x - self._radius > self._bounds.final_position.x:
                self._player_pos.x = self._bounds.initial_position.x + self._radius

        self._prev_points.append(self._player_pos.copy())
        if len(self._prev_points) > self._point:
            self._prev_points.pop(0)

    def update(self):
        self.__control_event()
        self.__move_engine()

    def __move_engine(self):
        tm = datetime.now() - self._prev_time
        speed = 200 * (5 / self._speed)
        if tm > timedelta(milliseconds=speed):
            self.__move()
            self._prev_time = datetime.now()

    def draw(self):
        for point in self._prev_points:
            self._sprite = pygame.draw.circle(self._screen, "black", point, self._radius+1)
            self._sprite = pygame.draw.circle(self._screen, "red", point, self._radius)
