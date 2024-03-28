import RPi.GPIO as GPIO
import time
import json
import threading

with open('params.json') as f:
    params = json.load(f)

left_buzzer = 5
right_buzzer = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_buzzer, GPIO.OUT)
GPIO.setup(right_buzzer, GPIO.OUT)

def left_event():
    with open('counter.json', 'r') as f:
        counter_data = json.load(f)
    # Increment the counter
    counter_data['counter'] += 1
    with open('counter.json', 'w') as f:
        json.dump(counter_data, f)
    #print("left_event")
    if params['use_buzzer'] == True:
        #print("left_buzzer")
        threading.Thread(target=left_buzzer_thread).start()        
    if params['use_sound'] == False and params['use_buzzer'] == False:
        pass

def right_event():
    #print("right_event")
 
    if params['use_buzzer'] == True:
        #print("right_buzzer")
        threading.Thread(target=right_buzzer_thread).start()    
    if params['use_sound'] == False and params['use_buzzer'] == False:
        pass

def left_buzzer_thread():
    GPIO.output(left_buzzer, GPIO.HIGH)
    time.sleep(0.11)
    GPIO.output(left_buzzer, GPIO.LOW)

def right_buzzer_thread():
    GPIO.output(right_buzzer, GPIO.HIGH)
    time.sleep(0.11)
    GPIO.output(right_buzzer, GPIO.LOW)