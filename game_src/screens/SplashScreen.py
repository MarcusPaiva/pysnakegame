import pygame
from pygame import Surface, SurfaceType

from game_engine.image_effects import fade_image
from game_engine.sound import SoundEffect
from game_src.screens.game_screens import GameScreen


class SplashScreen(GameScreen):
    def __init__(self, screen: Surface | SurfaceType):
        """
        Initialize splash screen.
        :param screen: Screen to show splash screen.
        """
        self._screen = screen
        self._logo = None
        self.logo_rect = None


    def setup(self) -> None:
        """
        Setup Splash Screen.
        :return:
        """
        self._logo = pygame.image.load(r'game_src/assets/images/logo/my_logo.png').convert_alpha()
        intro_sound = SoundEffect(r'./game_src/assets/sounds/effects/intro.mp3')
        intro_sound.play()
        self.logo_rect = self._logo.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))

    def loop(self) -> None:
        """
        Show splash screen event.
        """
        fade_image(self._screen, self._logo, self.logo_rect, 2500)

