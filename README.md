# PythonArtRgb

Color library that handles common art program blend modes as well as color wheel and saturation-value box visualizations.

Example Colorwheel:

| Color Wheel: | Color Box |
| --- | --- |
|![Colorwheel Example](examples/images/example_colorwheel.png) | ![Colorwheel Example ](examples/images/example_colorbox.png)
| Arrows are added corresponding to the Hue. Note the (overridable) -150 degree offset to match CSP. | Dots are placed corresponding to saturation (Y) and value (X)

| Sample Image| Swatch |
| --- | --- |
![](https://upload.wikimedia.org/wikipedia/commons/7/78/John_Singer_Sargent_-_Lady_Agnew_of_Lochnaw_-_Detail_1.jpg) | ![](examples/images/swatch.png)

## Usage

Supported construction

```python
Rgb()           # Defaults to black
Rgb(0,0,0)
Rgb((0,0,0))    # Supports tupple input
Rgb(0,0,0,0)    # Drops alpha channel for RGBA input
Rgb((0,0,0,0))
Rgb("black")    # uses PIL.ImageColor to handle named colors
```

Color blend modes:

```python
black = Rgb("black")
white = Rgb("white")
black + white
black - white
black * white
black / white
black.invert()
black.invert(white)
black.screen(white)
black.color_dodge(white)
black.linear_dodge(white)
black.hard_light(white)
black.overlay(white)
black.soft_light(white)
black.inv_soft_light(white)
```

HSV access

```python
black = Rgb("black")
black.rgb           # (0-255, 0-255, 0-255)
black.hsv           # (0-1, 0-1, 0-255)
black.hue           # 0-360
black.saturation    # 0-100
black.value         # 0-100
```
