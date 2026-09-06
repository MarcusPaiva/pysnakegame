from game_engine.image import Image
from game_engine.screen import SurfaceScreen
from game_engine.sound import SoundEffect
from game_src.screens.game_screens import GameScreen


class SplashScreen(GameScreen):
    def __init__(self, screen: SurfaceScreen):
        """
        Initialize splash screen.
        :param screen: Screen to show splash screen.
        """
        self._screen = screen
        self._logo = None


    def setup(self) -> None:
        """
        Setup Splash Screen.
        :return:
        """
        self._logo = Image(r'game_src/assets/images/logo/my_logo.png')
        intro_sound = SoundEffect(r'./game_src/assets/sounds/effects/intro.mp3')
        intro_sound.play()

    def loop(self) -> None:
        """
        Show splash screen event.
        """
        self._logo.fade(self._screen, 2500)

