from abc import ABC, abstractmethod

from game_engine.screen import SurfaceScreen


class GameScreen(ABC):
    """
    Game Screen interface.
    """

    @abstractmethod
    def __init__(self, screen: SurfaceScreen):
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