from typing import List

import pygame



class GameFont:
    def __init__(self, path:str, size:int, text:str):
        pygame.font.init()
        self.__text = text
        self.__font = pygame.font.Font(path,size)
        self.__color = [0,0,0]
        self.__anti_alias = False
        self.__background_color = None

    def get_text_size(self):
        return self.__font.size(self.__text)

    def set_text(self, text:str):
        self.__text = text
        return self

    def set_color(self, color:List[int]):
        self.__color = color
        return self

    def enable_anti_alias(self, value:bool):
        self.__anti_alias = value
        return self

    def set_background_color(self, value: "None|List[int]"):
        self.__background_color = value
        return self

    def render(self):
        return self.__font.render(self.__text, self.__anti_alias, self.__color, self.__background_color)