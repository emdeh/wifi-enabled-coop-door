try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (RuntimeError, ModuleNotFoundError):
    GPIO_AVAILABLE = False
    print("RPI.GPIO module not loaded. GPIO functionality will not be available.")

# Define the door pin as a global variable
door_pin = 23  # Change to your GPIO pin number if needed

def is_running_on_pi():
    # Check if the app is running on a Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as cpuinfo:
            return any("BCM" in line for line in cpuinfo if line.startswith('Hardware'))
    except IOError:
        return False  # /proc/cpuinfo does not exist, not running on a Pi

def setup_gpio():
    if is_running_on_pi() and GPIO_AVAILABLE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(door_pin, GPIO.OUT, initial=GPIO.HIGH)
        print("GPIO setup complete.")
    else:
        print("Not running on Raspberry Pi or RPI.GPIO module not loaded. GPIO functionality disabled.")

# Call setup_gpio() if running on a Raspberry Pi and GPIO is available
if GPIO_AVAILABLE and is_running_on_pi():
    setup_gpio()

def open_door():
    if GPIO_AVAILABLE:
        GPIO.output(door_pin, GPIO.LOW)  # Open the door
        print("Door open")
    else:
        print("Simulated Door Opened (No GPIO operation)")

def close_door():
    if GPIO_AVAILABLE:
        GPIO.output(door_pin, GPIO.HIGH)  # Close the door
        print("Door closed")
    else:
        print("Simulated Door Closed (No GPIO operation)")
