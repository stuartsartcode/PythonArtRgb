from PIL import Image, ImageDraw

from artrgb.color_box import ColorBox
from artrgb.rgb import Rgb

image_size = 500
box_size = 450
border = (image_size - box_size) // 2

img = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# box = ColorBox(box_size, Rgb("red"),)
box = ColorBox(image_size, box_size)

box.paste_into(img)

box.draw_dot(draw, Rgb("red"))
box.draw_dot(draw, Rgb("pink"))
box.draw_dot(draw, Rgb("salmon"))

img.save("examples/images/example_colorbox.png")
