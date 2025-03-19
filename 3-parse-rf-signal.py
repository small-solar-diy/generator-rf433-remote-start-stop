"""
3-parse-rf-signal.py

This script decodes RF signal data from a file, interpreting short and long pulses to determine
binary bits using Manchester encoding. It groups the decoded bits into sequences based on
long OFF periods, indicating the start of new transmissions.

"""

# Define timing thresholds
SHORT_MIN, SHORT_MAX = 200, 550      # Short pulse range (microseconds)
LONG_MIN, LONG_MAX = 800, 1550      # Long pulse range (microseconds)
LONG_OFF_THRESHOLD = 10000          # Reset sequence if OFF duration >= 10,000 microseconds

# Read the RF signal data
filename = "parsed_rf_signal.txt"  # Name of the file containing parsed RF signal data

# Load the data
signal_data = []  # List to store tuples of (signal, duration)

print("\n🔹 Step 1: Reading file...")
with open(filename, "r") as f:  # Open the file in read mode
    next(f)  # Skip the header line
    for line in f:  # Iterate through each line in the file
        parts = line.strip().split(", ")  # Remove leading/trailing whitespace and split by comma
        if len(parts) == 2:  # Ensure the line has two parts (signal and duration)
            try:
                signal, duration = int(parts[0]), int(parts[1])  # Convert signal and duration to integers
                signal_data.append((signal, duration))  # Add the (signal, duration) tuple to the list
            except ValueError:  # Handle invalid lines (non-integer values)
                print(f"⚠️ Skipping invalid line: {line.strip()}")
                continue  # Skip to the next line

print(f"✅ Loaded {len(signal_data)} signal entries\n")  # Print the number of loaded signal entries

# Step 2: Process signal pairs, restarting on LONG OFF
print("🔹 Step 2: Processing signal pairs...\n")
decoded_bits = []  # List to store decoded bit sequences
sequence = []  # List to store the current bit sequence
sequence_number = 1  # Counter for decoded sequences

# Iterate through signal pairs, excluding the last entry
for i in range(0, len(signal_data) - 1):
    sig1, dur1 = signal_data[i]  # Get the current signal and duration
    sig2, dur2 = signal_data[i + 1]  # Get the next signal and duration

    # Skip entries where the signal is 0 and the duration is less than the LONG_OFF_THRESHOLD
    if sig1 == 0 and dur1 < LONG_OFF_THRESHOLD:
        continue

    # Detect new transmission start (starts with a 1, long OFF period)
    if sig1 == 0 and dur1 >= LONG_OFF_THRESHOLD:
        if sequence:  # If a sequence is in progress, append it to decoded_bits
            decoded_bits.append(sequence)
            sequence_number += 1
        sequence = []  # Start a new sequence
        continue

    # Determine if it's a ONE or a ZERO based on Manchester encoding
    if sig1 == 1 and sig2 == 0:  # Ensure the signal order is 1 followed by 0
        is_part1_long = LONG_MIN <= dur1 <= LONG_MAX  # Check if the first duration is within the LONG range
        is_part1_short = SHORT_MIN <= dur1 <= SHORT_MAX  # Check if the first duration is within the SHORT range
        is_part2_long = LONG_MIN <= dur2 <= LONG_MAX  # Check if the second duration is within the LONG range
        is_part2_short = SHORT_MIN <= dur2 <= SHORT_MAX  # Check if the second duration is within the SHORT range

        # Identify bit value based on Manchester encoding rules
        if is_part1_long and is_part2_short:  # Long-Short pulse pair = 1
            bit = 1
        elif is_part1_short and is_part2_long:  # Short-Long pulse pair = 0
            bit = 0
        else:  # Handle unexpected pair durations
            continue  # Skip invalid pairs

        sequence.append(bit)  # Append the decoded bit to the current sequence

# Step 3: Print all decoded sequences
if sequence:  # Append the last sequence if it exists
    decoded_bits.append(sequence)

print("\n🔹 Final Decoded Sequences:")
for idx, seq in enumerate(decoded_bits, start=1):  # Iterate through the decoded sequences
    bit_sequence = ''.join(map(str, seq))  # Join the bits into a string
    digit_count = len(bit_sequence)  # Count the number of digits in the sequence
    print(f"{bit_sequence} - {digit_count}")  # Print the sequence and its length