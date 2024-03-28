import time
import board
import neopixel
import json

with open('params.json') as f:
    params = json.load(f)

brightness = params['brightness']
color_str = params['color']

color_dict = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
    'brown': (139, 69, 19),
    'light blue': (10, 186, 181),
    'white': (255, 255, 255)
}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return r, g, b

color = hex_to_rgb(color_str) if color_str.startswith("#") else color_dict.get(color_str, (0, 0, 0))

pixel_pin = board.D12
num_pixels = 47
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)

def focus():
    pixels.fill(color)
    pixels.show()

    time.sleep(0.1)

focus()