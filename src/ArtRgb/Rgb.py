# Implements blend modes defined in https://en.wikipedia.org/wiki/Blend_modes

import collections.abc
from colorsys import rgb_to_hsv, hsv_to_rgb
from math import sqrt
from PIL import ImageColor

def main():
    black = Rgb("black")
    white = Rgb("white")
    grey = Rgb("grey")
    brown = Rgb("brown")

    colors = [black, white, grey, brown]

    for li in range(len(colors)):
        ri = li + 1
        while ri < len(colors):
            l = colors[li]
            r = colors[ri]
            print("-----------------------------------")
            print(f"l: {l}\nr:{r}")
            print(f"  +: {l+r}, {r+l}")
            print(f"  -: {l-r}, {r-l}")
            print(f"  *: {l*r}, {r*l}")
            print(f"  /: {l/r}, {r/l}")
            print(f"  invert l: {l.invert()}")
            print(f"  invert r: {l.invert(r)}")
            ri +=1
            
class Rgb(collections.abc.Sequence):
    def __init__(self, *rgba: tuple):

        if len(rgba) == 0:
            self.rgb = (0,0,0)
        elif isinstance(rgba, str):
            self.rgb = tuple(int(x) for x in ImageColor.getrgb(rgba))
        elif len(rgba) == 1:
            if isinstance(rgba[0], str):
                self.rgb = tuple(int(x) for x in ImageColor.getrgb(rgba[0]))
            else:
                self.rgb = tuple(int(x) for x in rgba[0][:3])
        else:
            self.rgb = tuple(int(x) for x in rgba[:3])
        self.hsv = rgb_to_hsv(self.rgb[0], self.rgb[1], self.rgb[2])
        self.hue = int(self.hsv[0]*360)
        self.hue_rgb = tuple(int(x) for x in hsv_to_rgb(self.hsv[0], 1, 256))
        self.saturation = int(self.hsv[1]*100)
        self.value = int(self.hsv[2] /255 * 100)
    def __len__(self): return len(self.rgb)
    def __getitem__(self, index): return self.rgb[index]
    def __str__(self): return str(self.rgb)
    def __add__(self, r):
        return Rgb(denorm(add(norm(self), norm(r))))
    def __sub__(self, r):
        return Rgb(denorm(sub(norm(self), norm(r))))
    def __mul__(self, r):
        return Rgb(denorm(mul(norm(self), norm(r))))
    def __truediv__(self, r):
        return Rgb(denorm(div(self,r)))
    def invert(self, rgb = None):
        return Rgb(denorm(inv(rgb if rgb else self.rgb)))
    def screen(self, r):
        return Rgb(denorm(screen(norm(self), norm(r))))
    def color_dodge(self, r):
        return Rgb(denorm(color_dodge(norm(self), norm(r))))
    def linear_dodge(self, r):
        return Rgb(denorm(linear_dodge(norm(self), norm(r))))
    def hard_light(self, r):
        return Rgb(denorm(hard_light(norm(self), norm(r))))
    def overlay(self, r):
        return Rgb(denorm(hard_light(norm(self), norm(r))))
    def soft_light(self, r):
        return Rgb(denorm(soft_light(norm(self), norm(r))))
    def inv_soft_light(self, r):
        return Rgb(denorm(inv_soft_light(norm(self), norm(r))))

def norm(l) -> tuple:
    return tuple(a / 255.0 for a in l) 

def denorm(l) -> tuple:
    return tuple(max(0, min(255, int(a * 255.0))) for a in l) 

def bound(l) -> tuple:
    return tuple(max(0, min(1, a)) for a in l) 

def inv(l):
    return bound(1.0-a for a in norm(l))

def add(l, r):
    return bound(a+b for a,b in zip(l,r))

def sub(l, r):
    return bound(a-b for a,b in zip(l,r))

def avg(l, r):
    return bound((a+b)/2.0 for a,b in zip(l,r))

def mul(l, r):
    return bound(a*b for a,b in zip(l,r))

def div(l, r):
    return bound(
        a if b <= 0 else a/b for a, b in zip(l, r))
    
def screen(l,r):
    return inv(mul(inv(l), inv(r))) 

def color_dodge(l,r):
    return div(l, inv(r))

def linear_dodge(l,r):
    return add(l,r)

def overlay(l,r):
    return tuple( 
        # 2ab 
        2*a*b if a < .5 else
        # 1 - 2*(1-a)(1-b) 
        1-2*(1-a)*(1-b)
         for a,b in zip(l,r))
    
def hard_light(l,r):
    return tuple( 
        # 2ab 
        2*a*b if b < .5 else
        # 1 - 2*(1-a)(1-b) 
        1-2*(1-a)*(1-b) 
        for a,b in zip(l,r))

def soft_light(l,r):
    norml = tuple(a / 255 for a in l)
    normr = tuple(b / 255 for b in r)


    return bound(
        (1 - 2 * b) * a * a + 2 * b * a
        for a,b in zip(l, r)
    )

def soft_light_ps(l,r):
    return bound(
        # 2ab + a**2(1-2b)
        2 * a * b + a**2 * (1-2*b)
        if b < .5 else 
        2 * a *(1-b) + sqrt(a) * (2 * b - 1)
        for a,b in zip(l, r))
def inv_soft_light(l, r):
    return bound(
        1 if (-2 * a**2 + 2*a) == 0 else 
        (c - a**2) / (-2 * a**2 + 2*a)
        for a, c in zip(l, r)
    )

if __name__ == "__main__":
    main()