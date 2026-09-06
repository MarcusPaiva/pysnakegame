from abc import ABC, abstractmethod
from typing import Optional

from game_engine.bounding_box import BoundingBox


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
    def position(self) -> BoundingBox:
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
    def sprite(self) -> Optional[BoundingBox]:
        """
        Return GameObject's sprite.
        """
        pass