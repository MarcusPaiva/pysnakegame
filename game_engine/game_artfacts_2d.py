from typing import List

import pygame

from game_engine.bounding_box import RectBoundingBox, CircleBoundingBox


class Rect:
    def __init__(self, position_x:int, position_y:int, width:int, height:int):
        self.__bounding_box = RectBoundingBox(position_x, position_y, position_x + width, position_y + height)
        self.__fill_color = "red"

    def set_fill_color(self, color:"str|List[int]"):
        self.__fill_color = color
        return self

    def render(self, screen) -> RectBoundingBox:
        initial = self.__bounding_box.initial_position
        size = self.__bounding_box.size
        pygame.draw.rect(screen.get_screen(), self.__fill_color, [initial[0], initial[1], size[0], size[1]], 0)
        return self.__bounding_box.copy()

class Circle:
    def __init__(self, position_x:int, position_y:int, radius):
        self.__bounding_box = CircleBoundingBox(position_x, position_y, radius)
        self.__fill_color = "red"

    def set_fill_color(self, color:"str|List[int]"):
        self.__fill_color = color
        return self

    def render(self, screen) -> CircleBoundingBox:
        pygame.draw.circle(screen.get_screen(), self.__fill_color, self.__bounding_box.center, self.__bounding_box.radius)
        return self.__bounding_box.copy()
