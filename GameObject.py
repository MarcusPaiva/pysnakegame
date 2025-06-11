from abc import ABC, abstractmethod

import pygame
from pygame.rect import RectType, Rect


class GameObject(ABC):

    @abstractmethod
    def update(self):
        """
        Update GameObject event.
        :return:
        """
        pass

    @property
    @abstractmethod
    def position(self) -> pygame.Vector2:
        """
        GameObject current position.
        :return:
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        GameObject Draw event.
        """
        pass

    @property
    @abstractmethod
    def sprite(self) -> Rect | RectType | None:
        """
        Return GameObject's sprite.
        """
        pass