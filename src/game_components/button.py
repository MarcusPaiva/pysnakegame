from typing import Tuple

import pygame
from pygame import Surface, SurfaceType

from src.bounding_box import RectBoundingBox


def _mouse_click_detection() -> Tuple[int,int]:
    """
    Mouse click detection.
    :return: Mouse click position.
    """
    if pygame.mouse.get_pressed()[0]:
        return pygame.mouse.get_pos()

class Button:

    def __init__(self, screen:Surface | SurfaceType, start_x:int, start_y:int, text:str, margin:int=10, on_click = None, font_size:int = 40):
        """
        Button initializer.
        :param screen: Main screen instance.
        :param start_x: Axis x start position.
        :param start_y: Axis y end position.
        :param text: Text display.
        :param on_click: On click event.
        :param font_size: Text font size.
        """
        self._screen = screen
        self._margin = margin
        self._x = start_x
        self._y = start_y
        self._main_bounding_box = RectBoundingBox(start_x, start_y, 0, 0)
        self._text = text
        self._font_size = font_size
        self._main_font = None
        self._on_click = on_click
        self._background_color = "#cccccc"
        self._hover_color = "#000000"
        self._hover = False
        self._button_text = None
        self._text_position = [0,0]

    def setup(self):
        self._main_font = pygame.font.SysFont(r'./src/assets/fonts/roboto/Roboto-Black', 80)

    def _process_button_box(self):
        """Process button box"""
        x, y = self._main_font.size(f"{self._text}")
        width, height = (self._x + x + self._margin,
                         self._y + y + self._margin)
        self._main_bounding_box = RectBoundingBox(
            self._x - self._margin,
            self._y - self._margin,
            width,
            height
        )

    def background_color(self, color:str):
        """
        Set background color.
        :param color: Color hex.
        """
        self._background_color = color

    def hover_color(self, color:str):
        """
        Set hover background color.
        :param color: Color hex.
        """
        self._hover_color = color

    def update(self):
        self._process_button_box()
        mouse_click = _mouse_click_detection()
        if mouse_click is not None and self.__click_inside_button_detection(mouse_click[0],mouse_click[1]):
            if self._on_click is not None:
                self._on_click()
        self._hover = self.__mouse_hove_detection()
        self.__process_button_text()


    def __process_button_text(self):
        """
        Process button text.
        :return:
        """
        self._button_text: Surface = self._main_font.render(f'{self._text}', False, (255, 255, 255))
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = button_text_size[1] / 2
        center = self._main_bounding_box.center
        self._text_position = [center.x - text_center_x, center.y - text_center_y]

    def __mouse_hove_detection(self) -> bool:
        """
        Mouse move inside box detection event.
        :return: Mouse inside box status.
        """
        position_x, position_y = pygame.mouse.get_pos()
        box_bounds = self._main_bounding_box.bounds
        if box_bounds[0] < position_x < box_bounds[2] and box_bounds[1] < position_y < box_bounds[3]:
            return True

    def __click_inside_button_detection(self, position_x:int, position_y:int) -> bool:
        """
        Click inside box event.
        :param position_x: Axis x position event.
        :param position_y: Axis y position event.
        :return: Mouse click inside box status.
        """
        box_bounds = self._main_bounding_box.bounds
        if box_bounds[0] < position_x < box_bounds[2] and box_bounds[1] < position_y < box_bounds[3]:
            return True

    def draw(self) -> None:
        color = self._background_color
        if self._hover:
            color = self._hover_color
        pygame.draw.rect(
            self._screen,
            color, [
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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1100, 720))
    pygame.display.set_caption("User Button test")
    running = True
    clock = pygame.time.Clock()
    def click():
        print("clicked!")
    button = Button(screen, 200, 200, "Click Test!", on_click=click )
    button.setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("orange")
        button.update()
        button.draw()
        pygame.display.flip()
        clock.tick(60)



