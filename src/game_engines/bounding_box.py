from abc import ABC, abstractmethod
from typing import Tuple

import pygame


class BoundingBox(ABC):

    @property
    @abstractmethod
    def center(self) -> pygame.Vector2:
        """
        Get center's object.
        :return: Vector object.
        """
        pass

    @property
    @abstractmethod
    def initial_position(self) -> pygame.Vector2:
        """
        Get initial position.
        :return: Vector object with X0 and Y0.
        """
        pass

    @property
    @abstractmethod
    def final_position(self) -> pygame.Vector2:
        """
        Get initial position.
        :return: Vector object with X0 and Y0.
        """
        pass

    @property
    @abstractmethod
    def bounds(self) -> Tuple[int,int,int,int]:
        """
        Get bounds.
        :return: Tuple with bounds x start, y end, x final, and y final.
        """
        pass

    @property
    @abstractmethod
    def size(self) -> pygame.Vector2:
        """
        Get object's size.
        :return: Tuple with bounds x start, y end, x final, and y final.
        """
        pass

class RectBoundingBox(BoundingBox):
    def __init__(self, x0, y0, x, y):
        """
        BoundingBox initialize.
        :param x0: X initial.
        :param y0: Y initial.
        :param x: X final.
        :param y: Y final.
        """

        self._x0 = x0
        self._y0 = y0
        self._x = x
        self._y = y

    @property
    def center(self) -> pygame.Vector2:
        x_center = (self._x - self._x0) / 2
        y_center = (self._y - self._y0) / 2
        return pygame.Vector2(x_center + self._x0, y_center + self._y0)

    @property
    def initial_position(self) -> pygame.Vector2:
        return pygame.Vector2(self._x0, self._y0)

    @property
    def final_position(self) -> pygame.Vector2:
        return pygame.Vector2(self._x, self._y)

    @property
    def bounds(self) -> Tuple[int,int,int,int]:
        return self._x0, self._y0, self._x, self._y

    @property
    def size(self) -> pygame.Vector2:
        return pygame.Vector2(self._x - self._x0, self._y - self._y0)