import json

# Load and save configuration functions
def load_config():
    with open('configSettings.json', 'r') as file:
        return json.load(file)

def save_config(config):
    with open('configSettings.json', 'w') as file:
        json.dump(config, file, indent=4)