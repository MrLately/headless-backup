import time
import json
import l_r_events

with open('params.json') as f:
    params = json.load(f)

buzzer_wait = params['buzzer_wait']

def buzzer_pattern(buzzer_wait):
    while True:
        l_r_events.left_event()
        time.sleep(3.25 - buzzer_wait)
        l_r_events.right_event()
        time.sleep(3.25 - buzzer_wait)

# Start the buzzer pattern
buzzer_pattern(buzzer_wait)
