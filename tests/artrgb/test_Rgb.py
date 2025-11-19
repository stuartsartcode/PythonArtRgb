import pytest

from artrgb.rgb import Rgb


def test_rgb_creation():
    assert Rgb().rgb == (0,0,0)
    assert Rgb("black").rgb == (0,0,0)
    assert Rgb(("black")).rgb == (0,0,0)
    assert Rgb((0,0,0)).rgb == (0,0,0)
    assert Rgb(0,0,0).rgb == (0,0,0)
    assert Rgb((0,0,0,0)).rgb == (0,0,0)
    assert Rgb(0,0,0,0).rgb == (0,0,0)

    for bad_input in ["asdf", "", None, (), (-1), ("a", 255, 255)]:
        with pytest.raises(Exception):
            Rgb(bad_input)

def test_hsv():
    red = Rgb("red")
    assert red.hue == 0
    assert red.saturation == 100
    assert red.value == 100
    assert red.rgb == (255,0,0)
    assert red.hsv == (0,1,255)

def test_add():
    x = Rgb(10,10,10)
    y = Rgb(20,20,20)
    z = Rgb(30,30,30)
    
    assert x + x == y
    assert x + y == z
    assert y + x == z
    assert y - x == x
    assert x - y != x

@pytest.mark.parametrize("input_a, input_b", [("black", "white"), ("white", "black"), ("green", "blue"), ("red", "blue")])
def test_blend_modes(input_a:Rgb, input_b:Rgb):
    l = Rgb(input_a)
    r = Rgb(input_b)
    l.invert()
    l.invert(r)
    l.screen(r)
    l.color_dodge(r)
    l.linear_dodge(r)
    l.hard_light(r)
    l.overlay(r)
    l.soft_light(r)
    l.inv_soft_light(r)
    l.soft_light_ps(r)
    l.avg(r)
