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

    def render(self, screen):
        initial = self.__bounding_box.initial_position
        size = self.__bounding_box.size
        return pygame.draw.rect(screen, self.__fill_color, [initial.x, initial.y, size.x, size.y], 0)

class Circle:
    def __init__(self, position_x:int, position_y:int, radius):
        self.__bounding_box = CircleBoundingBox(position_x, position_y, radius)
        self.__fill_color = "red"

    def set_fill_color(self, color:"str|List[int]"):
        self.__fill_color = color
        return self

    def render(self, screen):
        return pygame.draw.circle(screen, self.__fill_color, self.__bounding_box.center, self.__bounding_box.radius)
