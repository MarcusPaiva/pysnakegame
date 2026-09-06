import pygame

from game_engine.image_effects import fade_image


class Image:
    def __init__(self, file:str):
        self.__image = pygame.image.load(file)

    def fade(self, screen, duration):
        self.__image.convert_alpha()
        logo_rect = self.__image.get_rect(center=(screen.width() // 2, screen.height() // 2))
        fade_image(screen, self.__image.convert_alpha(), logo_rect, duration)