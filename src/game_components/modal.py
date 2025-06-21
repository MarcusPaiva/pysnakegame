from dataclasses import dataclass, field
from typing import Callable, List

import pygame
from pygame import Surface, SurfaceType

from src.game_components.button import Button
from src.game_engines.bounding_box import RectBoundingBox


@dataclass
class Options:
    text: str
    on_click: Callable[[], None]
    background_color: str = field(default="#cccccc")
    hover_color: str = field(default="#cccccc")


class Modal:
    def __init__(self, screen: Surface | SurfaceType, start_x: int, start_y: int, text: str, end_x: int = 600,
                 end_y=400, margin: int = 10, font_size: int = 40, show=True):
        """
        Modal initializer.
        :param screen: Main screen instance.
        :param start_x: Axis x start position.
        :param start_y: Axis y end position.
        :param text: Text message inside modal to display.
        :param font_size: Text font size.
        """
        self._screen = screen
        self._margin = margin
        self._x = start_x
        self._y = start_y
        self._main_bounding_box = RectBoundingBox(start_x, start_y, start_x + end_x, start_y + end_y)
        self._text = text
        self._font_size = font_size
        self._main_font = None
        self._background_color = "#000000"
        self._margin_color = "red"
        self._options: List[Options] = []
        self._show = show
        self._options_buttons: List[Button] = []

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
        self._main_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', self._font_size)

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
        self.__process_button_text()
        self.__process_options()

    def __process_options(self):
        """
        Process options buttons in modal.
        :return:
        """
        self._options_buttons = []
        x,y = self._main_bounding_box.initial_position.xy
        end_x = self._main_bounding_box.final_position.x
        end_y = y + (self._main_bounding_box.size.y * 0.8)
        size_x = self._main_bounding_box.size.x
        x_step = 0
        if len(self._options) > 0:
         x_step = (size_x / len(self._options)) + self._margin
        for idx, option in enumerate(self._options):
            current_step = x + (x_step * idx) + (end_x * 0.12)
            btn = Button(self._screen,current_step, end_y, option.text,on_click=option.on_click)
            btn.hover_color(option.hover_color)
            btn.background_color(option.background_color)
            btn.disable(not self._show)
            btn.setup()
            btn.update()
            self._options_buttons.append(btn)

    def __process_button_text(self):
        """
        Process button text.
        :return:
        """
        self._button_text: Surface = self._main_font.render(f'{self._text}', False, (255, 255, 255))
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = self._main_bounding_box.final_position.y / 4
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
    modal = Modal(screen, 250, 150, "Game Over")
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
