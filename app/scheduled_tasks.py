from .hardware_control import open_door, close_door
import schedule
import time
from threading import Thread

# Scheduled job functions
def scheduled_open():
        open_door()

def scheduled_close():
        close_door()

# Initialize the scheduler
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Initialize and start the scheduler thread
scheduler_thread = Thread(target=run_schedule)
scheduler_thread.daemon = True  # This ensures that the thread will close when the main program exits
scheduler_thread.start()
