import pygame
from pygame import SurfaceType, Surface
import random

from pygame.rect import RectType, Rect

from GameObjects.GameObject import GameObject


class Fruit(GameObject):
    def __init__(self, screen: Surface | SurfaceType):
        self._screen = screen
        self._fruit_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
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
        self._fruit_pos.x = random.randint(self._radius, self._screen.get_width() - self._radius)
        self._fruit_pos.y = random.randint(self._radius, self._screen.get_height() - self._radius)

    def update(self):
        pass

    def draw(self):
        self._sprite = pygame.draw.circle(self._screen, "green", self._fruit_pos, self._radius)

