from dataclasses import dataclass, field

from PIL import ImageDraw

from artrgb.rgb import Rgb


@dataclass
class ColorDot:
    radius: int = field(default=10)
    fill_color: Rgb = field(default_factory=lambda: Rgb("white"))
    line_color: Rgb = field(default_factory=lambda: Rgb("black"))
    line_width: int = field(default=2)

    def draw(
        self,
        draw: ImageDraw.ImageDraw,
        xy: tuple[int, int],
        color: Rgb = None
    ):
        color = color if color else self.fill_color
        self.draw_dot(
            draw, xy, self.radius, color, self.line_color, self.line_width
        )

    @staticmethod
    def draw_dot(
        draw: ImageDraw.ImageDraw,
        xy=(0, 0),
        radius=10,
        fill_color=Rgb("white"),
        line_color=Rgb("black"),
        line_width=2,
    ):
        if line_width > 0:
            draw.circle(xy, radius + line_width, line_color)
        draw.circle(xy, radius, fill_color)
