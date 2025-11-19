import pytest
from ArtRgb.Rgb import Rgb

def test_rgb_creation():
    assert Rgb("black").rgb == (0,0,0)
    assert Rgb((0,0,0)).rgb == (0,0,0)
    assert Rgb(0,0,0).rgb == (0,0,0)
    assert Rgb((0,0,0,0)).rgb == (0,0,0)
    assert Rgb(0,0,0,0).rgb == (0,0,0)

    for input in ["asdf", "", None, (), (-1), ("a", 255, 255)]:
        with pytest.raises(Exception):
            Rgb(input)

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





