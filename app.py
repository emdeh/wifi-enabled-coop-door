from flask import Flask, request, jsonify, render_template
import RPi.GPIO as GPIO
import json
import schedule
import time
from threading import Thread

app = Flask(__name__, static_folder='static', template_folder='templates')

# GPIO setup
door_pin = 23  # Change to your GPIO pin number
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
    GPIO.output(door_pin, GPIO.LOW)  # Open the door
    print("Door opened")

# Function to close the door
def close_door():
    GPIO.output(door_pin, GPIO.HIGH)  # Close the door
    print("Door closed")

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
    
    if action == 'open':
        open_door()
        response = {'status': 'Door opened'}
    elif action == 'close':
        close_door()
        response = {'status': 'Door closed'}
    elif action == 'override':
        manual_override = not manual_override
        response = {'status': 'Manual override toggled', 'override': manual_override}
    else:
        response = {'status': 'Invalid action'}

    return jsonify(response)

# Route for handling read and writing settings.
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        global manual_override
        new_settings = request.json
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
