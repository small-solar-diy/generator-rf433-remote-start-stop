"""
2-process-signal.py

This script reads RF signal data from a text file, groups consecutive signal values with their durations,
and saves the parsed data to a new text file. It also filters out noise by ignoring signal changes
that last for fewer than a specified number of samples.

"""

# Load the RF signal data
filename = "rf_signal_data.txt"  # Name of the file containing the raw RF signal data

# Read the file and store time and signal values
timestamps = []  # List to store timestamps (microseconds)
signal_values = []  # List to store signal values (0 or 1)

print("** Reading RF Signal Data **")
with open(filename, "r") as f:  # Open the file in read mode ("r")
    next(f)  # Skip the header line ("Time (µs), Signal")
    for line in f:  # Iterate through each line in the file
        time, signal = line.strip().split(", ")  # Remove leading/trailing whitespace and split the line by comma
        timestamps.append(int(time))  # Convert the time string to an integer (microseconds) and append it to the timestamps list
        signal_values.append(int(signal))  # Convert the signal string to an integer (0 or 1) and append it to the signal_values list

print(f"Total samples read: {len(timestamps)}\n")  # Print the total number of samples read from the file

# Process and group signal durations
grouped_signals = []  # List to store tuples of (signal, duration)
start_time = timestamps[0]  # Initialize the start time with the first timestamp
current_signal = signal_values[0]  # Initialize the current signal with the first signal value
sample_count = 0  # Initialize the sample count to 0

# Variables to handle noise filtering
previous_duration = 0  # Store the previous duration
previous_signal = 0  # Store the previous signal
previous_time = 0    # store the previous time
previous_sample = 0  # store the previous sample count
noise_sample = 4  # Threshold for noise filtering (signal changes shorter than this are considered noise)

print(f"Current start time: {start_time}")  # Print the initial start time

# Iterate through the timestamps and signal values, starting from the second sample
for i in range(1, len(timestamps)):
    sample_count += 1  # Increment the sample count
    if signal_values[i] != current_signal and sample_count > noise_sample:  # Check for signal change and if the signal change is longer than noise_sample
        duration = timestamps[i - 1] - start_time  # Calculate the duration of the current signal
        grouped_signals.append((current_signal, duration))  # Append the (signal, duration) tuple to the grouped_signals list
        start_time = timestamps[i]  # Update the start time to the current timestamp
        current_signal = signal_values[i]  # Update the current signal to the new signal value
        print(f"{i}: Sample Count:{sample_count} Duration:{duration} Current Signal:{current_signal}") #Print debug info
        sample_count = 0  # Reset the sample count
    elif signal_values[i] != current_signal and sample_count < noise_sample: # signal is noise, rollback to previous values
        duration = previous_duration
        start_time = previous_time
        current_signal = previous_signal
        sample_count = previous_sample
    else: # store values for possible rollback
        previous_duration = timestamps[i-1] - start_time
        previous_signal = current_signal
        previous_time = start_time
        previous_sample = sample_count

# Add the last group
grouped_signals.append((current_signal, timestamps[-1] - start_time))  # Append the last (signal, duration) tuple

# Save the result to a file
with open("parsed_rf_signal.txt", "w") as f:  # Open the output file in write mode ("w")
    f.write("Signal, Duration (µs)\n")  # Write the header row
    for signal, duration in grouped_signals:  # Iterate through the grouped_signals list
        f.write(f"{signal}, {duration}\n")  # Write each (signal, duration) pair to a new line

print("\n** Parsing Complete **")  # Print a message indicating the parsing is complete
print("Grouped signal data saved to parsed_rf_signal.txt")  # Print the filename where the parsed data is saved