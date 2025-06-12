import sys

import pygame
from pygame import Surface, SurfaceType

def fade_logo(screen, logo, logo_rect, duration=2000):
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

class SplashScreen:
    def __init__(self, screen: Surface | SurfaceType):
        self._screen = screen
        self._logo = pygame.image.load(r'src/assets/images/logo/my_logo.png').convert_alpha()

    def show(self):
        logo_rect = self._logo.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        fade_logo(self._screen,self._logo,logo_rect, 2500)

