import pytest
from artrgb.color_box import ColorBox
from artrgb.rgb import Rgb
from PIL import Image, ImageDraw


def test_create_box():

    image_size = 500
    box_size = 450
    img = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    box = ColorBox(image_size, box_size)
    box.paste_into(img)
    box.draw_dot(draw, Rgb("red"))
    box.draw_dot(draw, Rgb("pink"))
    box.draw_dot(draw, Rgb("salmon"))
