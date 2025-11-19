from dataclasses import dataclass, field

from PIL import ImageDraw

from artrgb.rgb import Rgb


@dataclass
class ColorDot:
    radius: int = field(default=10)
    fill: Rgb = field(default_factory=lambda: Rgb("white"))
    border_color: Rgb = field(default_factory=lambda: Rgb("black"))
    border_width: int = field(default=2)

    def draw(
        self,
        draw: ImageDraw.ImageDraw,
        xy: tuple[int, int],
        fill_override: Rgb = None,
        border_override: Rgb = None,
        radius_override: int = None,
    ):
        radius = radius_override if radius_override else self.radius
        border_color = self.border_color if not border_override else border_override
        fill_color = self.fill if not fill_override else fill_override
        if self.border_width > 0:
            draw.circle(xy, radius, border_color.rgb)
        draw.circle(xy, radius - self.border_width, fill_color.rgb)
