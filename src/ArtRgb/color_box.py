#
# A tool to create Clip Studio Paint styled Hue/Saturation boxes
#
from colorsys import hsv_to_rgb
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageDraw

from artrgb.color_dot import ColorDot
from artrgb.rgb import Rgb


@dataclass
class ColorBox:
    size: int  # Size of box excluding border
    box_size: int  # Box size excluding border and line_width
    dest: tuple = field(default=(0, 0))
    hue: Rgb = field(default_factory=lambda: Rgb("red"))
    line_width: int = field(default=4)
    line_fill: Rgb = field(default_factory=lambda: Rgb())
    dot: ColorDot = field(default_factory=lambda: ColorDot())

    def __post_init__(self):
        self.border = (self.size - self.box_size - 2 * self.line_width) // 2

    def paste_into(self, image: Image.Image, dest: tuple = None):
        dest = dest if dest else self.dest
        lined_box = self.box_size + 2 * self.line_width
        box = Image.new("RGBA", (lined_box, lined_box), color=self.line_fill.rgb)
        box.alpha_composite(
            SatValColor(self.box_size, self.hue), (self.line_width, self.line_width)
        )
        image.alpha_composite(box, tuple(x + self.border for x in dest))

    def draw_dot(
        self,
        draw: ImageDraw.ImageDraw,
        color: Rgb,
        dot_size: int = None,
        use_hue=False,
        dest: tuple = None,
    ):
        color = color if isinstance(color, Rgb) else Rgb(color)
        dot_size = dot_size if dot_size else self.dot.radius
        fill_rgb = color.hue_rgb if use_hue else color
        dest = dest if dest else self.dest
        dot_xy = self.get_dot_point(color, dest)

        self.dot.draw_dot(draw, dot_xy, dot_size, fill_rgb)

    def get_dot_point(self, color: Rgb, dest: tuple = None):
        if not dest:
            dest = self.dest
        rel_xy = self.get_color_rel_xy(color, self.box_size)
        x = dest[0] + self.border + rel_xy[0] + self.line_width
        y = dest[1] + self.border + rel_xy[1] + self.line_width
        return (x, y)

    @staticmethod
    def get_color_rel_xy(color: Rgb, size: int):
        saturation = color.saturation * size // 100
        value = size - color.value * size // 100
        return (saturation, value)


def SatValColor(size, swatch_color: Rgb) -> Image:
    # Use RGBA for alpha compositing later
    img = Image.new("RGBA", (size, size), color="white")
    hue = swatch_color.hsv[0]
    sat = np.linspace(0.0, 1.0, size)
    val = np.linspace(255.0, 0.0, size)
    draw = ImageDraw.Draw(img)
    for y in range(size):
        for x in range(size):
            draw.point((x, y), tuple(int(x) for x in hsv_to_rgb(hue, sat[x], val[y])))
    return img
