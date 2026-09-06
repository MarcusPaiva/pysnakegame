from dataclasses import dataclass, field
from typing import Callable, List

import pygame
from pygame import Surface, SurfaceType

from game_src.game_components.button import Button
from game_engine.bounding_box import RectBoundingBox
from game_engine.font import GameFont


@dataclass
class Options:
    text: str
    on_click: Callable[[], None]
    background_color: str = field(default="#cccccc")
    hover_color: str = field(default="#cccccc")


class Modal:
    def __init__(self, screen: Surface | SurfaceType, text: str, width_ratio: float = 0.6,
                 height_ratio: float = 0.55, margin: int = 10, font_size: int = 40, show=True):
        """
        Modal initializer.
        :param screen: Main screen instance.
        :param text: Text message inside modal to display.
        :param width_ratio: Modal width as a fraction of the screen's current width.
        :param height_ratio: Modal height as a fraction of the screen's current height.
        :param font_size: Text font size.
        """
        self._screen = screen
        self._margin = margin
        self._width_ratio = width_ratio
        self._height_ratio = height_ratio
        self._main_bounding_box = self.__compute_bounding_box()
        self._text = text
        self._font_size = font_size
        self._main_font = None
        self._background_color = "#000000"
        self._margin_color = "red"
        self._options: List[Options] = []
        self._show = show
        self._options_buttons: List[Button] = []

    def __compute_bounding_box(self) -> RectBoundingBox:
        """
        Compute a bounding box centered on the screen, sized proportionally
        to the screen's current dimensions.
        :return: Centered RectBoundingBox.
        """
        screen_width = self._screen.get_width()
        screen_height = self._screen.get_height()
        width = screen_width * self._width_ratio
        height = screen_height * self._height_ratio
        x0 = (screen_width - width) / 2
        y0 = (screen_height - height) / 2
        return RectBoundingBox(x0, y0, x0 + width, y0 + height)

    def show(self, value:bool):
        """
        Display modal.
        :param value: Visibility status.
        :return:
        """
        self._show = value

    def setup(self):
        """
        Setup event.
        """
        self._main_font = GameFont(
            r'./game_src/assets/fonts/roboto/Roboto-Black.ttf', self._font_size, self._text
        ).set_color([255, 255, 255])

    def add_options(self, options: List[Options]):
        """
        Add options to modal.
        :param options: List of options to add in modal.
        :return:
        """
        self._options += options

    def update(self):
        """
        Update event.
        """
        self._main_bounding_box = self.__compute_bounding_box()
        self.__process_button_text()
        self.__process_options()

    def __process_options(self):
        """
        Process options buttons in modal, laid out left-to-right with equal
        gaps between them and equal outer margins to the box's edges,
        regardless of how wide each button's text makes it.
        :return:
        """
        self._options_buttons = []
        if not self._options:
            return

        x, y = self._main_bounding_box.initial_position.xy
        end_y = y + (self._main_bounding_box.size.y * 0.8)
        size_x = self._main_bounding_box.size.x

        buttons = []
        for option in self._options:
            btn = Button(self._screen, 0, end_y, option.text, margin=self._margin, on_click=option.on_click)
            btn.hover_color(option.hover_color)
            btn.background_color(option.background_color)
            btn.disable(not self._show)
            btn.setup()
            buttons.append(btn)

        widths = [btn.content_size().x for btn in buttons]
        gap = self._margin
        total_width = sum(widths) + gap * (len(buttons) - 1)
        outer_margin = max((size_x - total_width) / 2, 0)

        current_left = x + outer_margin
        for btn, width in zip(buttons, widths):
            btn.set_position(current_left + self._margin, end_y)
            btn.update()
            self._options_buttons.append(btn)
            current_left += width + gap

    def __process_button_text(self):
        """
        Process button text.
        :return:
        """
        self._button_text: Surface = self._main_font.render()
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = self._main_bounding_box.size.y * 0.35
        center = self._main_bounding_box.center
        self._text_position = [center.x - text_center_x, center.y - text_center_y]

    def draw(self):
        """
        Draw event.
        """
        if self._show:
            pygame.draw.rect(
                self._screen,
                self._margin_color, [
                    self._main_bounding_box.initial_position.x,
                    self._main_bounding_box.initial_position.y,
                    self._main_bounding_box.size.x,
                    self._main_bounding_box.size.y
                ],
                0,
            )

            pygame.draw.rect(
                self._screen,
                self._background_color, [
                    self._main_bounding_box.initial_position.x,
                    self._main_bounding_box.initial_position.y,
                    self._main_bounding_box.size.x,
                    self._main_bounding_box.size.y
                ],
                0,
            )

            self._screen.blit(
                self._button_text,
                self._text_position
            )
            for option in self._options_buttons:
                option.draw()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1100, 720))
    pygame.display.set_caption("User Button test")
    running = True
    clock = pygame.time.Clock()
    modal = Modal(screen, "Game Over")
    def confirm():
        print("Confirm")

    def dismiss():
        print("Dismiss!")
        modal.show(False)
    options = [
        Options("Confirm", confirm, "green", "white"),
        Options("Dismiss", dismiss, "red", "white"),
    ]
    modal.add_options(options)

    modal.setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("orange")
        modal.update()
        modal.draw()
        pygame.display.flip()
        clock.tick(60)
