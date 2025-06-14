import sys

import pygame
from pygame import Surface, SurfaceType

from src.screens.game_screens import GameScreen


def fade_logo(screen, logo, logo_rect, duration=2000):
    """
    Fade effect to display images.
    :param screen: Screen to show image.
    :param logo: Logo to display.
    :param logo_rect: Logo bounds.
    :param duration: Effect duration.
    """
    clock = pygame.time.Clock()
    alpha_surface = pygame.Surface(logo.get_size(), pygame.SRCALPHA)

    fade_in_time = duration // 2
    fade_out_time = duration // 2

    elapsed = 0
    fade_in = True

    while elapsed < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60)
        elapsed += dt

        if fade_in:
            alpha = min(255, int((elapsed / fade_in_time) * 255))
            if elapsed >= fade_in_time:
                fade_in = False
                elapsed = 0
        else:
            alpha = max(0, 255 - int((elapsed / fade_out_time) * 255))

        alpha_surface.fill((255, 255, 255, 0))
        alpha_surface.blit(logo, (0, 0))
        alpha_surface.set_alpha(alpha)

        screen.fill("white")
        screen.blit(alpha_surface, logo_rect)
        pygame.display.flip()

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
        self._logo = pygame.image.load(r'src/assets/images/logo/my_logo.png').convert_alpha()
        intro_sound = pygame.mixer.Sound(r'./src/assets/sounds/effects/intro.mp3')
        intro_sound.play()
        self.logo_rect = self._logo.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))

    def loop(self) -> None:
        """
        Show splash screen event.
        """
        fade_logo(self._screen,self._logo, self.logo_rect, 2500)

