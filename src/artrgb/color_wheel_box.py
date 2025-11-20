# Combination of Color Wheel and Color Box

from math import sqrt
from dataclasses import dataclass, field
from artrgb.color_dot import ColorDot
from artrgb.rgb import Rgb
from artrgb.color_box import ColorBox
from artrgb.color_wheel import ColorWheel
from PIL import ImageDraw, Image


@dataclass
class ColorWheelBox:
    size: int
    wheel_size: int
    box_size: int
    dest: tuple = field(default=(0, 0))
    box_hue: Rgb = field(default_factory=lambda: Rgb("red"))
    line_width: int = field(default=4)

    def __post_init__(self):
        self.hole_size = (self.box_size + 2 * self.line_width) * sqrt(2)
        print(self.hole_size)
        self.color_wheel = ColorWheel(
            self.size, self.wheel_size, self.hole_size, self.line_width
        )
        self.color_box = ColorBox(self.size, self.box_size, self.box_hue)

    def paste_into(self, image: Image.Image, dest=None):
        if not dest:
            dest = self.dest
        self.color_wheel.paste_into(image, dest)
        self.color_box.paste_into(image, dest)

    def draw_color(
        self,
        draw: ImageDraw.ImageDraw,
        color: Rgb,
        dest: tuple = None,
        # dot: ColorDot = None,
        dot_size=10,
        arrow_length=30,
        arrow_from_hole=True,
    ):
        if not dest:
            dest = self.dest
        if dot_size != 0:
            self.color_box.draw_dot(draw, color, dot_size, False, dest)
        if arrow_length != 0:
            self.color_wheel.draw_arrow(
                draw, color, dest, arrow_length, from_hole=arrow_from_hole
            )
