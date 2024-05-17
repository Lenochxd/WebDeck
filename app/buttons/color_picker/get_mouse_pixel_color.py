import numpy as np
import mss
from pyautogui import position
from PIL import Image


def get_mouse_pixel_color():
    x, y = position()

    # Gets the screenshot of each monitor and compares the cursor position to determine the screen
    for i, monitor in enumerate(mss.mss().monitors):
        if (
            monitor["left"] <= x < monitor["left"] + monitor["width"]
            and monitor["top"] <= y < monitor["top"] + monitor["height"]
        ):
            monitor_index = i
            break

    # Take screenshot of specific screen
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        img = sct.grab(monitor)
        screenshot = np.array(
            Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        )

    # Gets the color of the pixel under the mouse cursor
    color = screenshot[y - monitor["top"], x - monitor["left"]]

    # Convert color to HEX format
    hex_color = "#{:02x}{:02x}{:02x}".format(*color)

    # Convert color to RGB format
    rgb_color = "rgb({},{},{})".format(*color)

    # Convert color to HSL format
    r, g, b = [x / 255.0 for x in color]
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = ((g - b) / delta) % 6
    elif cmax == g:
        hue = (b - r) / delta + 2
    else:
        hue = (r - g) / delta + 4

    hue = round(hue * 60)
    if hue < 0:
        hue += 360

    lightness = (cmax + cmin) / 2
    saturation = 0 if delta == 0 else delta / (1 - abs(2 * lightness - 1))

    hsl_color = "hsl({}, {:.2f}%, {:.2f}%)".format(
        hue, saturation * 100, lightness * 100
    )
    
    
    return {
        "hex": hex_color,
        "rgb": rgb_color,
        "hsl": hsl_color
    }