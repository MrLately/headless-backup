import time
import board
import neopixel
import json
import random
import l_r_events

with open('params.json') as f:
    params = json.load(f)

brightness = params['brightness']
slide_wait = params['slide_wait']
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

def random_color():
    return random.choice(list(color_dict.values()))

pixel_pin = board.D12
num_pixels = 47
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)

def custom_animation():
    while True:
        # Slide pattern
        for _ in range(2):
            block_size = random.randint(1, min(3, num_pixels))
            color = random_color()

            direction = 'right'
            if block_size == 1:
                adjusted_slide_wait = slide_wait
            elif block_size == 2:
                speed_reduction_factor = 0.4
                adjusted_slide_wait = slide_wait * speed_reduction_factor
            elif block_size == 3:
                speed_reduction_factor = 0.2
                adjusted_slide_wait = slide_wait * speed_reduction_factor

            for i in range(0, num_pixels, block_size):
                pixels.fill((0, 0, 0))
                start_idx = min(i, num_pixels - block_size)
                for j in range(block_size):
                    pixels[start_idx + j] = tuple(
                        int(val * (j + 1) / block_size) for val in color
                    )
                pixels.show()
                time.sleep(0.01 - adjusted_slide_wait)

                if i == 0 and direction == 'right':
                    # Left event logic
                    direction = 'left'
                    l_r_events.left_event()
                elif i + block_size >= num_pixels and direction == 'left':
                    # Right event logic
                    direction = 'right'
                    l_r_events.right_event()

            for i in range(num_pixels - block_size, -1, -block_size):
                pixels.fill((0, 0, 0))
                for j in range(block_size):
                    if i - j >= 0:
                        pixels[i - j] = tuple(
                            int(val * (j + 1) / block_size) for val in color
                        )
                pixels.show()
                time.sleep(0.01 - adjusted_slide_wait)

        # Blink pattern
        for _ in range(2):
            block_size = random.randint(1, min(23, num_pixels))
            color = random_color()

            led_state = 'right'

            for _ in range(2):
                pixels.fill((0, 0, 0))
                pixels[:block_size] = [color] * block_size
                pixels[-block_size:] = [(0, 0, 0)] * block_size
                pixels.show()

                if led_state != 'left':
                    # Left event logic
                    led_state = 'left'
                    l_r_events.left_event()
                time.sleep(3.25 - blink_wait)

                pixels.fill((0, 0, 0))
                pixels[-block_size:] = [color] * block_size
                pixels[:block_size] = [(0, 0, 0)] * block_size
                pixels.show()

                if led_state != 'right':
                    # Right event logic
                    led_state = 'right'
                    l_r_events.right_event()
                time.sleep(3.25 - blink_wait)

custom_animation()