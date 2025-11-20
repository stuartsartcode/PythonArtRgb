from PIL import Image, ImageDraw

from artrgb.color_wheel import ColorWheel
from artrgb.rgb import Rgb

image_size = 500
wheel_size = 400
wheel_hole = 200

img = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

wheel = ColorWheel(500, 400, 200, border_color=Rgb("black"), line_width=4)
wheel.paste_into(img)

offset = (0, 0)
wheel.draw_arrow(draw, Rgb("red"), offset)
wheel.draw_arrow(draw, Rgb("pink"), offset)
wheel.draw_arrow(draw, Rgb("salmon"), offset)

img.save("examples/images/example_colorwheel.png")
