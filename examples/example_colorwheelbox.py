from PIL import Image, ImageDraw
from artrgb.color_wheel_box import ColorWheelBox
from artrgb.rgb import Rgb

image_size = 500
wheel_size = 400
box_size = 200
# wheel_hole = 200

img = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)


wheelbox = ColorWheelBox(image_size, wheel_size, box_size)
wheelbox.paste_into(img)

colors = ["red", "pink", "salmon"]

dot_size_start = 10
dot_size_modifier = 3
arrow_length_start = 30
arrow_length_modifier = 10
for i in reversed(range(len(colors))):
    color = Rgb(colors[i])
    dot_size = dot_size_start + (len(colors) - i - 1) * dot_size_modifier
    arrow_length = arrow_length_start + (len(colors) - i - 1) * arrow_length_modifier
    wheelbox.draw_color(
        draw, color, dot_size=dot_size, arrow_length=arrow_length, arrow_from_hole=False
    )

for i in reversed(range(len(colors))):
    color = Rgb(colors[i])
    dot_size = 1
    arrow_length = 0
    wheelbox.draw_color(draw, color, dot_size=dot_size, arrow_length=arrow_length)

img.save("examples/images/example_colorwheelbox.png")
