from datetime import datetime, timedelta
from typing import List

import pygame
from pygame import SurfaceType, Surface
from pygame.rect import RectType, Rect

from game_engine.GameObject import GameObject
from game_engine.bounding_box import BoundingBox
from game_engine.game_artfacts_2d import Circle
from game_engine.inputs.game_input import Keyboard, Keys
from game_engine.sound import SoundEffect


class Player(GameObject):
    def __init__(self, screen:Surface | SurfaceType, game_bounds:BoundingBox):
        self._screen = screen
        self._bounds = game_bounds
        self._player_pos = self._bounds.center
        self._speed = 3
        self._last_position = Keys.up
        self._radius = 10
        self._sprite = None
        self._point = 1
        self._prev_points = [self._player_pos]
        self._eat_effect = SoundEffect(r'./game_src/assets/sounds/effects/eating.mp3').set_volume(0.7)
        self._prev_time = datetime.now()
        self._game_keyboard = Keyboard()

    @property
    def points(self):
        return self._point

    def add_point(self):
        self._eat_effect.play()
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
        if Keys.key_up in keys and not self._last_position == Keys.up:
            self._last_position = Keys.up
        if Keys.key_down in keys and not self._last_position == Keys.down:
            self._last_position = Keys.down
        if Keys.key_left in keys and not self._last_position == Keys.left:
            self._last_position = Keys.left
        if Keys.key_right in keys and not self._last_position == Keys.right:
            self._last_position = Keys.right

    def __move(self):
        # Why does this code create mental knots?
        if self._last_position == Keys.up:
            self._player_pos.y -= self._radius * 2 + 3
            if self._player_pos.y - self._radius < self._bounds.initial_position.y:
                self._player_pos.y = self._bounds.final_position.y - self._radius
        if self._last_position == Keys.down:
            self._player_pos.y += self._radius * 2 + 3
            if self._player_pos.y + self._radius > self._bounds.final_position.y:
                self._player_pos.y = self._bounds.initial_position.y + self._radius
        if self._last_position == Keys.left:
            self._player_pos.x -= self._radius * 2 + 3
            if self._player_pos.x - self._radius < self._bounds.initial_position.x:
                self._player_pos.x = self._bounds.final_position.x - self._radius
        if self._last_position == Keys.right:
            self._player_pos.x += self._radius * 2 + 3
            if self._player_pos.x + self._radius > self._bounds.final_position.x:
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
            self._sprite = Circle(point.x, point.y, self._radius + 1).set_fill_color("black").render(self._screen)
            self._sprite = Circle(point.x, point.y, self._radius).set_fill_color("red").render(self._screen)
