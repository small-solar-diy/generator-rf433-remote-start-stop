"""
1-collect-signal.py

This script records a digital signal received on a specified GPIO pin of a Raspberry Pi.
It captures the timestamps and signal values for a defined duration and saves the data to a text file.

Press the start button continually before and after the collection is running
Keep the remote very close to the receiver (6") and less noise is captured

"""

from datetime import datetime  # Import the datetime module for timestamping (not currently used, but potentially useful for logging)
import RPi.GPIO as GPIO  # Import the RPi.GPIO library for interacting with GPIO pins
import sys  # Import the sys module (not currently used, but potentially useful for command-line arguments)
import time  # Import the time module for time-related functions
from collections import deque  # Import deque for efficient append operations (faster than lists for growing data)

# Constants
RECEIVE_PIN = 12  # GPIO pin number where the signal is received
MAX_DURATION = 5  # Maximum duration of recording in seconds
RECEIVED_SIGNAL = [deque(), deque()]  # Initialize a list containing two deques:
                                        #   - RECEIVED_SIGNAL[0]: Stores timestamps (microseconds)
                                        #   - RECEIVED_SIGNAL[1]: Stores signal values (0 or 1)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM (Broadcom SOC channel numbers)
GPIO.setup(RECEIVE_PIN, GPIO.IN)  # Configure the receive pin as an input

# Start time
start_time_ns = time.time_ns()  # Record the start time in nanoseconds
print("**Started recording**")  # Print a message indicating the start of recording

# Recording loop
while (time.time_ns() - start_time_ns) < (MAX_DURATION * 1_000_000_000):  # Loop until the specified duration is reached
    current_time_ns = time.time_ns()  # Get the current time in nanoseconds
    RECEIVED_SIGNAL[0].append(int((current_time_ns - start_time_ns) / 1_000))  # Calculate elapsed time in microseconds, convert to int, and append to the timestamp deque
    RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))  # Read the signal value from the receive pin and append it to the signal values deque

print("**Ended recording**")  # Print a message indicating the end of recording
print(len(RECEIVED_SIGNAL[0]), "samples recorded")  # Print the number of recorded samples

GPIO.cleanup()  # Clean up GPIO settings to release resources

# Convert deque to lists
time_microseconds = list(RECEIVED_SIGNAL[0])  # Convert the timestamp deque to a list
signal_values = list(RECEIVED_SIGNAL[1])  # Convert the signal values deque to a list

# Save data to a text file
filename = "rf_signal_data.txt"  # Define the filename for the output text file
with open(filename, "w") as f:  # Open the file in write mode ("w")
    f.write("Time (µs), Signal\n")  # Write the header row to the file
    for t, s in zip(time_microseconds, signal_values):  # Iterate through the timestamps and signal values simultaneously
        f.write(f"{t}, {s}\n")  # Write each timestamp and signal value pair to a new line in the file

print(f"Data saved to {filename}")  # Print a message indicating the data has been saved
