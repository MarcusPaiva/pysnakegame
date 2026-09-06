from datetime import datetime, timedelta
from typing import List

from pygame.rect import RectType, Rect

from game_engine.GameObject import GameObject
from game_engine.bounding_box import BoundingBox, CircleBoundingBox
from game_engine.game_artfacts_2d import Circle
from game_engine.inputs.game_input import Keyboard, Keys
from game_engine.screen import SurfaceScreen
from game_engine.sound import SoundEffect


class Player(GameObject):
    def __init__(self, screen:SurfaceScreen, game_bounds:BoundingBox):
        self._screen = screen
        self._bounds = game_bounds
        self._speed = 3
        self._last_position = Keys.up
        self._radius = 10
        self._position = CircleBoundingBox(self._bounds.center_x, self._bounds.center_y, self._radius)
        self._sprite = None
        self._point = 1
        self._prev_points = [self._position.copy()]
        self._eat_effect = SoundEffect(r'./game_src/assets/sounds/effects/eating.mp3').set_volume(0.7)
        self._prev_time = datetime.now()
        self._game_keyboard = Keyboard()

    @property
    def points(self):
        return self._point

    def add_point(self):
        self._eat_effect.play()
        self._point += 1
        self._speed += self._speed * (self._point / 1000)

    @points.setter
    def points(self, point:int):
        self._point = point


    @property
    def position(self) -> CircleBoundingBox:
        return self._position

    @property
    def positions(self) -> List[CircleBoundingBox]:
        return self._prev_points

    @property
    def radius(self):
        return self._radius

    @property
    def sprite(self) -> Rect | RectType | None:
        return self._sprite

    def __control_event(self):
        self._game_keyboard.detect_buttons()
        keys = self._game_keyboard.current_keys_pressing
        if Keys.key_up in keys and not self._last_position == Keys.up:
            self._last_position = Keys.up
        if Keys.key_down in keys and not self._last_position == Keys.down:
            self._last_position = Keys.down
        if Keys.key_left in keys and not self._last_position == Keys.left:
            self._last_position = Keys.left
        if Keys.key_right in keys and not self._last_position == Keys.right:
            self._last_position = Keys.right

    def __move(self):
        # Why does this code create mental knots?
        if self._last_position == Keys.up:
            self._position.move_by(0, -(self._radius * 2 + 3))
            if self._position.y0 < self._bounds.y0:
                self._position.set_position(self._position.center_x, self._bounds.y1 - self._radius)
        if self._last_position == Keys.down:
            self._position.move_by(0, self._radius * 2 + 3)
            if self._position.y1 > self._bounds.y1:
                self._position.set_position(self._position.center_x, self._bounds.y0 + self._radius)
        if self._last_position == Keys.left:
            self._position.move_by(-(self._radius * 2 + 3), 0)
            if self._position.x0 < self._bounds.x0:
                self._position.set_position(self._bounds.x1 - self._radius, self._position.center_y)
        if self._last_position == Keys.right:
            self._position.move_by(self._radius * 2 + 3, 0)
            if self._position.x1 > self._bounds.x1:
                self._position.set_position(self._bounds.x0 + self._radius, self._position.center_y)

        self._prev_points.append(self._position.copy())
        if len(self._prev_points) > self._point:
            self._prev_points.pop(0)

    def update(self):
        self.__control_event()
        self.__move_engine()

    def __move_engine(self):
        tm = datetime.now() - self._prev_time
        speed = 200 * (5 / self._speed)
        if tm > timedelta(milliseconds=speed):
            self.__move()
            self._prev_time = datetime.now()

    def draw(self):
        for point in self._prev_points:
            self._sprite = Circle(point.center_x, point.center_y, self._radius + 1).set_fill_color("black").render(self._screen)
            self._sprite = Circle(point.center_x, point.center_y, self._radius).set_fill_color("red").render(self._screen)
