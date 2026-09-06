"""
Text rendering wrapper around :mod:`pygame.font`.
"""
from typing import List

import pygame


class GameFont:
    """
    A loaded font bound to one piece of text, with configurable color,
    anti-aliasing and background, that can be re-rendered on demand.
    """

    def __init__(self, path: str, size: int, text: str):
        """
        :param path: Path to a ``.ttf`` font file.
        :param size: Font size, in points.
        :param text: Initial text to render.
        """
        pygame.font.init()
        self.__text = text
        self.__font = pygame.font.Font(path, size)
        self.__color = [0, 0, 0]
        self.__anti_alias = False
        self.__background_color = None

    def get_text_size(self):
        """
        Measure the current text as it would be rendered, without
        actually rendering it.

        :return: ``(width, height)`` of the rendered text, in pixels.
        :rtype: Tuple[int, int]
        """
        return self.__font.size(self.__text)

    def set_text(self, text: str):
        """
        Change the text this font renders.

        :param text: New text.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__text = text
        return self

    def set_color(self, color: List[int]):
        """
        Set the text color.

        :param color: ``[r, g, b]`` (or ``[r, g, b, a]``) color.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__color = color
        return self

    def enable_anti_alias(self, value: bool):
        """
        Toggle anti-aliasing for subsequent renders.

        :param value: Whether to anti-alias the rendered text.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__anti_alias = value
        return self

    def set_background_color(self, value: "None|List[int]"):
        """
        Set (or clear) the background color drawn behind the text.

        :param value: ``[r, g, b]`` background color, or None for a
            transparent background.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__background_color = value
        return self

    def render(self):
        """
        Render the current text with the current color, anti-alias and
        background settings.

        :return: The rendered text.
        :rtype: pygame.Surface
        """
        return self.__font.render(self.__text, self.__anti_alias, self.__color, self.__background_color)
