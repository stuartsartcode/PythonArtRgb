from colorsys import hsv_to_rgb
from dataclasses import dataclass, field
from math import cos, radians, sin

from PIL import Image, ImageDraw

from artrgb.rgb import Rgb


@dataclass
class ColorWheel:
    size: int
    wheel_size: int
    inner_hole: int = field(default=0)
    line_width: int = field(default=0)
    use_sat_val: bool = field(default=False)
    border_color: Rgb = field(default_factory=lambda: Rgb())
    coun: int = field(default=360)
    hue_angle_offset: int = field(default=-150)

    def __post_init__(self):
        self.mid_point = self.size // 2

    def paste_into(self, image: Image.Image, dest: tuple = (0, 0)):
        # mid_point = self.size//2
        wheel_image = Image.new("RGBA", (self.size, self.size))
        draw = ImageDraw.Draw(wheel_image)
        # Draw border
        if self.line_width > 0:
            # line_start = (self.size - self.wheel_size)//2 - self.line_width
            draw.circle(
                (self.mid_point, self.mid_point),
                self.wheel_size // 2 + self.line_width,
                fill=self.border_color.rgb,
            )
        # Draw color_wheel

        wheel_offset = (self.size - self.wheel_size) // 2
        wheel_image.alpha_composite(
            colorwheel(self.wheel_size), (wheel_offset, wheel_offset)
        )
        # Draw hole
        if self.inner_hole > 0:
            if self.line_width > 0:
                draw.circle(
                    (self.mid_point, self.mid_point),
                    self.inner_hole // 2,
                    fill=self.border_color.rgb,
                )
            draw.circle(
                (self.mid_point, self.mid_point),
                self.inner_hole // 2 - self.line_width,
                fill=(0, 0, 0, 0),
            )
        image.alpha_composite(wheel_image, dest)


    def draw_arrow(
        self,
        draw: ImageDraw.ImageDraw,
        colors: Rgb,
        dest: tuple,
        arrow_length=30,
        arrow_degrees=30,
        from_hole=False,
        bar_fill=Rgb(),
    ):
        colors = [colors] if isinstance(colors, Rgb) else colors
        for hue in reversed(colors):
            bar_length = (self.size - self.inner_hole) // 2
            degree = hue.hue + self.hue_angle_offset
            arrow_dir = degree
            # arrow_dir += 180

            line_colors = ["black", hue.rgb]
            for i in range(len(line_colors)):
                color = line_colors[i]
                line_offset = 8 * i
                radius = (
                    (self.inner_hole // 2) - self.line_width
                    if from_hole
                    else (self.wheel_size // 2 + self.line_width)
                ) + line_offset
                # line_colors = ["black", hue.rgb]
                x = dest[0] + self.mid_point + cos(radians(degree)) * radius
                y = dest[1] + self.mid_point + sin(radians(degree)) * radius

                offset_length = arrow_length - line_offset

                # print(f"drawing color {color}")
                # for t in ["i", "color", "line_offset", "radius", "x", "y", "offset_length"]:
                #     print(f"- {t}: {locals()[t]}")

                pi_radius = arrow_length - 1.5 * line_offset

                bbox = (x - pi_radius, y - pi_radius, x + pi_radius, y + pi_radius)
                draw.pieslice(
                    bbox,
                    arrow_dir - (arrow_degrees - 6 * i) // 2,
                    arrow_dir + (arrow_degrees - 6 * i) // 2,
                    color,
                )

    def get_arrow_point(
        self, color: Rgb, dest: tuple = (0, 0), hue_angle_offset=-150
    ) -> tuple:
        degree = color.hue + hue_angle_offset
        arrow_dir = degree
        radius = self.inner_hole // 2
        # line_colors = ["black", hue.rgb]
        x = dest[0] + self.mid_point + cos(radians(degree)) * radius
        y = dest[1] + self.mid_point + sin(radians(degree)) * radius
        return (x, y)

    @staticmethod
    def get_hue_rotation_xy(color: Rgb, radius: int):
        # -150 to match CSP.
        degree = color.hue - 150
        x = int(cos(radians(degree)) * radius)
        y = int(sin(radians(degree)) * radius)
        return (x, y)


def colorwheel(size, hue: Rgb | None = None, use_sat_val=False, count=360):
    image = Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    seg_length = int(360 / count)
    offset = -150
    start = offset - seg_length // 2 - 1
    for i in range(count):
        # color
        degree = i * seg_length

        if not hue or not use_sat_val:
            rgb = tuple(int(x) for x in hsv_to_rgb(degree / 360.0, 1, 255))
        else:
            hsv = hue[0].hsv
            rgb = tuple(int(x) for x in hsv_to_rgb(degree / 360.0, hsv[1], hsv[2]))

        end = degree + offset + seg_length // 2
        # print(locals())
        draw.pieslice([(0, 0), (size, size)], start=start, end=end, fill=rgb)
        start = end
    return image