from typing import List

import pygame
from pygame import SurfaceType, Surface
from pygame.rect import RectType, Rect

from GameObject import GameObject


class Player(GameObject):
    def __init__(self, screen:Surface | SurfaceType, time_delta:int):
        self._time_delta = time_delta
        self._screen = screen
        self._player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self._speed = 300
        self._last_position = pygame.K_w
        self._radius = 10
        self._sprite = None
        self._point = 1
        self._prev_points = [self._player_pos]

    def add_point(self):
        self._point += 1

    def set_point(self, point:int):
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

    # def set_time_delta(self, dt:int):
    #     self._time_delta = dt

    def __control_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not self._last_position == pygame.K_w:
            self._last_position = pygame.K_w
        if keys[pygame.K_s] and not self._last_position == pygame.K_s:
            self._last_position = pygame.K_s
        if keys[pygame.K_a] and not self._last_position == pygame.K_a:
            self._last_position = pygame.K_a
        if keys[pygame.K_d] and not self._last_position == pygame.K_d:
            self._last_position = pygame.K_d

    def __move(self):
        last = self._player_pos.copy()
        if self._last_position == pygame.K_w:
            self._player_pos.y -= self._radius * 2 + 3
            if self._player_pos.y - self._radius < 0:
                self._player_pos.y = self._screen.get_height() + self._radius
        if self._last_position == pygame.K_s:
            self._player_pos.y += self._radius * 2 + 3
            if self._player_pos.y + self._radius > self._screen.get_height():
                self._player_pos.y = self._radius * 2
        if self._last_position == pygame.K_a:
            self._player_pos.x -= self._radius * 2 + 3
            if self._player_pos.x - self._radius < 0:
                self._player_pos.x = self._screen.get_width() - self._radius
        if self._last_position == pygame.K_d:
            self._player_pos.x += self._radius * 2 + 3
            if self._player_pos.x - self._radius > self._screen.get_width():
                self._player_pos.x = self._radius

        self._prev_points.append(self._player_pos.copy())
        if len(self._prev_points) > self._point:
            self._prev_points.pop(0)

    def update(self):
        self.__control_event()

    def move(self):
        self.__move()

    def draw(self):
        for point in self._prev_points:
            self._sprite = pygame.draw.circle(self._screen, "black", point, self._radius+1)
            self._sprite = pygame.draw.circle(self._screen, "red", point, self._radius)
