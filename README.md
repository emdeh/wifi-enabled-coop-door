# To do

## Setup the Raspberry Pi:

- Install the operating system (Raspbian) and set up the network so that the Raspberry Pi is accessible over your network. *Done*
- Enable SSH for remote access to the Raspberry Pi terminal. *Done*

## Create the Web Interface:

- Use a web framework like Flask or Django to create a web server that will run on the Raspberry Pi and serve your dashboard. *Partially Done*

## Interface with the GPIO Pins:

- Write Python scripts to interface with the GPIO pins that control the chicken coop door. You'll use the RPi.GPIO library for this purpose. *Partially Done*
- Create functions for opening and closing the door, and for setting and checking the door's current status. *Partially Done*


## Remote Control Functionality:

- Implement AJAX in your web interface to send commands to your Raspberry Pi server without needing to refresh the page. 
- Define routes in your Flask or Django app that will listen for these commands and call the appropriate Python functions to control the door. *Partially Done*

## Timer Functionality:

- Use a job scheduler like cron or a Python library like schedule to manage the door's opening and closing times. *Done*
- Provide the functionality in your web interface to update these schedules. *Done*


## Manual Override:

- Ensure your web interface can send a manual override command that is prioritized over scheduled actions. *Partially Done*
- Implement logic in your Python code that can handle this override. *Partially Done*


## Configuration Settings:

- Use a JSON file or a database to store user preferences and settings, like the timer schedule. *Partially Done*
- Make sure your web interface can update and retrieve these settings. *Done*

## Testing:

- Before connecting to the actual door mechanism, test your setup with LEDs or other indicators to simulate door actions.
- Ensure that all safety features are in place to prevent harm to the chickens, such as implementing a soft start/stop for the door movement and ensuring that the door cannot close if an obstacle is detected.


## Security Considerations:

- Implement authentication for the web interface to prevent unauthorized access.
- Consider using HTTPS to encrypt communication with the Raspberry Pi.

# Next up

- Need to fix triggers to when scheduled time passes, the door open functions are called.