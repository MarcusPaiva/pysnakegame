import pygame
from pygame import SurfaceType, Surface
import random

from pygame.rect import RectType, Rect

from src.GameObjects.GameObject import GameObject
from src.game_engines.bounding_box import BoundingBox


class Fruit(GameObject):
    def __init__(self, screen: Surface | SurfaceType, game_bounds:BoundingBox):
        self._screen = screen
        self._bounds = game_bounds
        self._fruit_pos = pygame.Vector2(self._bounds.final_position.x / 2, self._bounds.final_position.y / 2)
        self._radius = 10
        self._sprite = None

    @property
    def position(self) -> pygame.Vector2:
        return self._fruit_pos

    @property
    def radius(self):
        return self._radius

    @property
    def sprite(self) -> Rect | RectType | None:
        return self._sprite

    def generate(self):
        """
        Generate new point
        :return:
        """
        self._fruit_pos.x = random.randint(int(self._bounds.initial_position.x) + self._radius, int(self._bounds.final_position.x) - self._radius)
        self._fruit_pos.y = random.randint(int(self._bounds.initial_position.y) + self._radius, int(self._bounds.final_position.y) - self._radius)

    def update(self):
        pass

    def draw(self):
        self._sprite = pygame.draw.circle(self._screen, "green", self._fruit_pos, self._radius)

