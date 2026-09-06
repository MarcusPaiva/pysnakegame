from abc import ABC, abstractmethod

from pygame import Surface, SurfaceType


class GameScreen(ABC):
    """
    Game Screen interface.
    """

    @abstractmethod
    def __init__(self, screen: Surface | SurfaceType):
        """
        Game Scree initializer.
        :param screen: Screen window.
        """
        pass

    @abstractmethod
    def setup(self) -> None:
        """
        Setup game screen event.
        """
        pass

    @abstractmethod
    def loop(self) -> None:
        """
        Loop game screen event.
        """