import time

def debounce(pin):
    # Read the initial state of the pin
    last_state = pin.value
    # Wait for the signal to stabilize
    time.sleep(0.01)
    # Read the state of the pin again
    current_state = pin.value
    # Check if the state has changed
    if last_state != current_state:
        # Wait for the signal to stabilize again
        time.sleep(0.01)
        # Read the state of the pin one more time
        current_state = pin.value
    # Return the debounced state of the pin
    return current_state