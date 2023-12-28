from flask import Flask, request, jsonify, render_template
import json
import schedule
import time
from threading import Thread
import os

def is_running_on_pi():
    """check if the app is running on a raspberry pi."""
    try:
        with open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Hardware') and 'BCM' in line:
                    return True
    except IOError:
        # /proc/cpuinfo does not exist, not running on a Pi
        return False
    
# Conditionally import the GPIO library
if is_running_on_pi():
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
else:
    print("RPI.GPIO module not loaded. GPIO functionality will not be available.")
    GPIO_AVAILABLE = False

app = Flask(__name__, static_folder='static', template_folder='templates')

# GPIO setup
door_pin = 23  # Change to your GPIO pin number

if GPIO_AVAILABLE:
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setup(door_pin, GPIO.OUT, initial=GPIO.HIGH)

# Global variable for manual override
manual_override = False

# Load and save configuration functions
def load_config():
    with open('configSettings.json', 'r') as file:
        return json.load(file)

def save_config(config):
    with open('configSettings.json', 'w') as file:
        json.dump(config, file, indent=4)

# Function to open the door
def open_door():
    if GPIO_AVAILABLE:
        GPIO.output(door_pin, GPIO.LOW)  # Open the door
        print("Door cpen")
    else:
        print("Simulated Door Opened (No GPIO operation)")

# Function to close the door
def close_door():
    if GPIO_AVAILABLE:
        GPIO.output(door_pin, GPIO.HIGH)  # Close the door
        print("Door closed")
    else:
        print("Simulated Door Closed (No GPIO operation)")

# Scheduled job functions
def scheduled_open():
    if not manual_override:
        open_door()

def scheduled_close():
    if not manual_override:
        close_door()

# Initialize the scheduler
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler thread
scheduler_thread = Thread(target=run_schedule)
scheduler_thread.daemon = True  # This ensures that the thread will close when the main program exits
scheduler_thread.start()

# Route for serving the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling door control
@app.route('/door', methods=['POST'])
def control_door():
    global manual_override
    data = request.json
    action = data.get('action')
    
    # Check if manual_override is enabled before proceeding
    if not manual_override:
        return jsonify({'status': 'Override not enabled, action not allowed'}), 403
    
    if action == 'open':
        open_door()
        response = {'status': 'Door OPENED'}
    elif action == 'close':
        close_door()
        response = {'status': 'Door CLOSED'}
    else:
        response = {'status': 'Invalid action'}

    return jsonify(response)

# Route for handling manual override toggle
@app.route('/override', methods=['POST'])
def toggle_override():
    global manual_override
    data = request.json
    manual_override = data.get('override', False)
    
    # Perform any needed actions when override status changes
    if manual_override:
        # Logic to cancel scheduled jobs can go here
        schedule.clear()
    else:
        # Logic to set up scheduled jobs again can go here
        # Setup the initial schedule from the config file
        config = load_config()
        schedule.every().day.at(config['door']['open_time']).do(scheduled_open)
        schedule.every().day.at(config['door']['close_time']).do(scheduled_close)
    
    response = {
        'status': 'Override status updated',
        'override': manual_override
    }
    return jsonify(response)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        new_settings = request.json
        print("Received new settings:", new_settings)  # Debugging print
        save_config(new_settings)

        # Update the schedule based on new settings
        schedule.clear()
        if not manual_override:
            schedule.every().day.at(new_settings['door']['open_time']).do(scheduled_open)
            schedule.every().day.at(new_settings['door']['close_time']).do(scheduled_close)

        return jsonify({'status': 'Settings updated'})

    elif request.method == 'GET':
        current_settings = load_config()
        return jsonify(current_settings)


if __name__ == '__main__':
    # Setup the initial schedule from the config file
    config = load_config()
    schedule.every().day.at(config['door']['open_time']).do(scheduled_open)
    schedule.every().day.at(config['door']['close_time']).do(scheduled_close)
    
    app.run(host='0.0.0.0', port=5000)
