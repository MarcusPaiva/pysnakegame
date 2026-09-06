import random

from pygame.rect import RectType, Rect

from game_engine.GameObject import GameObject
from game_engine.bounding_box import BoundingBox, CircleBoundingBox
from game_engine.game_artfacts_2d import Circle
from game_engine.screen import SurfaceScreen


class Fruit(GameObject):
    def __init__(self, screen: SurfaceScreen, game_bounds:BoundingBox):
        self._screen = screen
        self._bounds = game_bounds
        self._radius = 10
        self._position = CircleBoundingBox(self._bounds.x1 / 2, self._bounds.y1 / 2, self._radius)
        self._sprite = None

    @property
    def position(self) -> CircleBoundingBox:
        return self._position

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
        x = random.randint(int(self._bounds.x0) + self._radius, int(self._bounds.x1) - self._radius)
        y = random.randint(int(self._bounds.y0) + self._radius, int(self._bounds.y1) - self._radius)
        self._position.set_position(x, y)

    def update(self):
        pass

    def draw(self):
        self._sprite = Circle(self._position.center_x, self._position.center_y, self._radius).set_fill_color("green").render(self._screen)

