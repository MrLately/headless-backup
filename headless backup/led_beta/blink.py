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
blink_wait = params['blink_wait']

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

def blink_pattern(brightness, color, block_size, blink_wait):
    led_state = 'right'
    
    while True:
        pixels.fill((0, 0, 0))
        pixels[:block_size] = [color] * block_size
        pixels[-block_size:] = [0, 0, 0]
        pixels.show()
        
        if led_state != 'left':
            l_r_events.left_event()
            led_state = 'left'
        time.sleep(3.25 - blink_wait)  # Reverse the blink wait time here
        
        pixels.fill((0, 0, 0))
        pixels[-block_size:] = [color] * block_size
        pixels[:block_size] = [0, 0, 0]
        pixels.show()
        
        if led_state != 'right':
            l_r_events.right_event()
            led_state = 'right'
        time.sleep(3.25 - blink_wait)  # Reverse the blink wait time here

blink_pattern(brightness, color, block_size, blink_wait)
