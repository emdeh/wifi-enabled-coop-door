from flask import render_template, jsonify, request
from flask_login import login_required
from .hardware_control import open_door, close_door
from .utilities import load_config, save_config

def configure_routes(app):
    
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.route('/door', methods=['POST'])
    @login_required
    def control_door():
        data = request.json
        action = data.get('action')

        if action == 'open':
            open_door()
            response = {'status': 'OPENED'}
        elif action == 'close':
            close_door()
            response = {'status': 'CLOSED'}
        else:
            response = {'status': 'Invalid action'}

        return jsonify(response)

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def settings():
        if request.method == 'POST':
            new_settings = request.json
            save_config(new_settings)
            # Update the schedule based on new settings
            # Call a function from scheduled_tasks.py to update the schedule
            return jsonify({'status': 'Settings updated'})
        elif request.method == 'GET':
            current_settings = load_config()
            return jsonify(current_settings)
