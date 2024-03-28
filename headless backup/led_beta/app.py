from flask import Flask, render_template, request, jsonify
import board
import neopixel
import RPi.GPIO as GPIO
import json
import subprocess
import logging
import time

# Configure logging to capture errors and other messages
#log_file_path = 'app_log.txt'  # Specify the path to the log file

#logging.basicConfig(
#    filename=log_file_path,
#    level=logging.DEBUG,  # Set the logging #level to control which messages are captured
#    format='%(asctime)s - %(levelname)s - %(message)s'
#)

app = Flask(__name__)

left_buzzer = 5
right_buzzer = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_buzzer, GPIO.OUT)
GPIO.setup(right_buzzer, GPIO.OUT)

with open('params.json') as f:
    params = json.load(f)

brightness = float(params['brightness'])
color = params['color']
block_size = params['block_size']
blink_wait = params['blink_wait']
slide_wait = params['slide_wait']
buzzer_wait = params['buzzer_wait']
                        
pixel_pin = board.D12
num_pixels = 47
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)

current_animation_process = None
animation_running = False

@app.route('/api/get_counter', methods=['GET'])
def get_counter():
    with open('counter.json', 'r') as f:
        counter_data = json.load(f)
    return jsonify(counter=counter_data['counter'])

@app.route('/api/reset_counter', methods=['POST'])
def reset_counter():
    data = request.json
    counter_data = {'counter': 0}
    with open('counter.json', 'w') as f:
        json.dump(counter_data, f)
    return jsonify(success=True)

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return response

@app.route('/')
def index():
    global current_animation_process
    animation_running = current_animation_process is not None
    return render_template('index.html', params=params, animation_running=animation_running)

@app.route('/api/update_params', methods=['POST'])
def update_params():
    new_params = request.get_json()
    params.update(new_params)
    with open('params.json', 'w') as f:
        json.dump(params, f)
    return jsonify(success=True)

@app.route('/api/start_animation', methods=['POST'])
def start_animation():
    global selected_animation, current_animation_process, animation_running
    if current_animation_process:
        stop_current_animation()
    selected_animation = params['selected_animation']
    if selected_animation == "blink":
        current_animation_process = subprocess.Popen(["python3", "blink.py"])
    elif selected_animation == "slide":
        current_animation_process = subprocess.Popen(["python3", "slide.py"])
    elif selected_animation == "attent":
        current_animation_process = subprocess.Popen(["python3", "attention.py"])
    elif selected_animation == "buzzer":
        current_animation_process = subprocess.Popen(["python3", "buzzer.py"])
    animation_running = True
    return jsonify(success=True)

@app.route('/api/stop_animation', methods=['POST'])
def stop_animation():
    global current_animation_process, animation_running
    stop_current_animation()
    GPIO.output(left_buzzer, GPIO.LOW)
    GPIO.output(right_buzzer, GPIO.LOW)
    pixels.fill((0, 0, 0,))
    pixels.show()
    animation_running = False
    return jsonify(success=True)

@app.route('/api/focus_animation', methods=['POST'])
def focus_animation():
    global selected_animation, current_animation_process, animation_running
    if current_animation_process:
        if selected_animation == "buzzer" or selected_animation == "attent":
            return jsonify(success=False, message="Buzzer animation is running, focus animation ignored")
        stop_current_animation()        
        focus_process = subprocess.Popen(["python3", "focus.py"])
        focus_process.wait()
        if selected_animation == "blink":
            current_animation_process = subprocess.Popen(["python3", "blink.py"])
        elif selected_animation == "slide":
            current_animation_process = subprocess.Popen(["python3", "slide.py"])        
        animation_running = True
        return jsonify(success=True)

@app.route('/api/update_buzzer', methods=['POST'])
def update_buzzer():
    new_buzzer_value = request.get_json().get('use_buzzer', False)
    params['use_buzzer'] = new_buzzer_value
    with open('params.json', 'w') as f:
        json.dump(params, f)
    return jsonify(success=True)

def select_animation_type(new_selected_animation):
    global selected_animation
    selected_animation = new_selected_animation

def stop_current_animation():
    global pixels, left_buzzer, right_buzzer, current_animation_process
    if current_animation_process:
        current_animation_process.terminate()
        current_animation_process = None
        GPIO.output(left_buzzer, GPIO.LOW)
        GPIO.output(right_buzzer, GPIO.LOW)
        pixels.fill((0, 0, 0,))
        pixels.show()
    # Code to stop the animation

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)