import time
import board
import neopixel
import json
import l_r_events

with open('params.json') as f:
    params = json.load(f)

brightness = params['brightness']
color_str = params['color']
block_size = params['block_size']
slide_wait = 0.01 - params['slide_wait']

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

def sliding_motion(brightness, color, block_size, slide_wait):
    position = 0
    direction = 1
    speed_factor = 1.0 / block_size  # Adjust the speed based on block size
    adjusted_slide_wait = slide_wait * speed_factor
    left_triggered = False
    right_triggered = False
    
    while True:
        pixels.fill((0, 0, 0))

        if position + block_size <= num_pixels and position >= 0:
            pixels[position:position + block_size] = [color] * block_size

        pixels.show()

        if position <= 0 and not left_triggered:
            l_r_events.left_event()
            left_triggered = True
            right_triggered = False
        elif position + block_size >= num_pixels and not right_triggered:
            l_r_events.right_event()
            right_triggered = True
            left_triggered = False

        position += direction

        if position + block_size > num_pixels or position < 0:
            direction *= -1

        time.sleep(adjusted_slide_wait)

sliding_motion(brightness, color, block_size, slide_wait)