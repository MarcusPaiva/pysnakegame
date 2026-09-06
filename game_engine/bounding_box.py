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

    @property
    @abstractmethod
    def x0(self) -> float:
        """
        Left edge (or bounding-square left, for a circle) as a plain number.
        """
        pass

    @property
    @abstractmethod
    def y0(self) -> float:
        """
        Top edge (or bounding-square top, for a circle) as a plain number.
        """
        pass

    @property
    @abstractmethod
    def x1(self) -> float:
        """
        Right edge (or bounding-square right, for a circle) as a plain number.
        """
        pass

    @property
    @abstractmethod
    def y1(self) -> float:
        """
        Bottom edge (or bounding-square bottom, for a circle) as a plain number.
        """
        pass

    @property
    @abstractmethod
    def center_x(self) -> float:
        """
        Center x coordinate as a plain number.
        """
        pass

    @property
    @abstractmethod
    def center_y(self) -> float:
        """
        Center y coordinate as a plain number.
        """
        pass

    @property
    @abstractmethod
    def width(self) -> float:
        """
        Width as a plain number.
        """
        pass

    @property
    @abstractmethod
    def height(self) -> float:
        """
        Height as a plain number.
        """
        pass

    @abstractmethod
    def copy(self) -> "BoundingBox":
        """
        Return an independent copy of this bounding box.
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

    @property
    def x0(self) -> float:
        return self._x0

    @property
    def y0(self) -> float:
        return self._y0

    @property
    def x1(self) -> float:
        return self._x

    @property
    def y1(self) -> float:
        return self._y

    @property
    def center_x(self) -> float:
        return self._x0 + (self._x - self._x0) / 2

    @property
    def center_y(self) -> float:
        return self._y0 + (self._y - self._y0) / 2

    @property
    def width(self) -> float:
        return self._x - self._x0

    @property
    def height(self) -> float:
        return self._y - self._y0

    def copy(self) -> "RectBoundingBox":
        return RectBoundingBox(self._x0, self._y0, self._x, self._y)


class CircleBoundingBox(BoundingBox):
    def __init__(self, x_center:int, y_center:int, radius:int):
        self.__x = x_center
        self.__y = y_center
        self.__radius = radius

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.__x,self.__y)

    @property
    def initial_position(self) -> pygame.Vector2:
        return pygame.Vector2(self.__x - self.__radius,self.__y - self.__radius)

    @property
    def final_position(self) -> pygame.Vector2:
        return pygame.Vector2(self.__x + self.__radius,self.__y + self.__radius)

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        return self.__x - self.__radius,self.__y - self.__radius, self.__x + self.__radius,self.__y + self.__radius

    @property
    def size(self) -> pygame.Vector2:
        return pygame.Vector2(self.__radius, self.__radius)

    @property
    def radius(self):
        return self.__radius

    @property
    def x0(self) -> float:
        return self.__x - self.__radius

    @property
    def y0(self) -> float:
        return self.__y - self.__radius

    @property
    def x1(self) -> float:
        return self.__x + self.__radius

    @property
    def y1(self) -> float:
        return self.__y + self.__radius

    @property
    def center_x(self) -> float:
        return self.__x

    @property
    def center_y(self) -> float:
        return self.__y

    @property
    def width(self) -> float:
        return self.__radius * 2

    @property
    def height(self) -> float:
        return self.__radius * 2

    def copy(self) -> "CircleBoundingBox":
        return CircleBoundingBox(self.__x, self.__y, self.__radius)

    def set_position(self, x: float, y: float) -> "CircleBoundingBox":
        """
        Move this circle's center to an absolute position.
        :param x: New center x.
        :param y: New center y.
        """
        self.__x = x
        self.__y = y
        return self

    def move_by(self, dx: float, dy: float) -> "CircleBoundingBox":
        """
        Move this circle's center by a relative offset.
        :param dx: X offset.
        :param dy: Y offset.
        """
        self.__x += dx
        self.__y += dy
        return self

    def __eq__(self, other) -> bool:
        if not isinstance(other, CircleBoundingBox):
            return NotImplemented
        return (self.__x, self.__y, self.__radius) == (other.center_x, other.center_y, other.radius)

    def __hash__(self):
        return hash((self.__x, self.__y, self.__radius))
