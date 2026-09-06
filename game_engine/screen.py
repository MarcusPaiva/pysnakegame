from typing import List

import pygame


class SurfaceScreen:
    def __init__(self, width:int, height:int, title:str):
        self.__screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()

    def draw(self, artfact, position:List[int]):
        self.__screen.blit(artfact, position)
        return self

    def fill(self, color:"str|List[int]"):
        self.__screen.fill(color)
        return self

    def height(self):
        return self.__screen.get_height()

    def width(self):
        return self.__screen.get_width()

    def flip(self):
        pygame.display.flip()
        return self

    def set_clock(self, value:int):
        self._clock.tick(value)
        return self

    def get_screen(self):
        return self.__screen