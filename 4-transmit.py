import time
import sys
import RPi.GPIO as GPIO

# code generatrice
start = '111000000111001110100001'
stop = '111000000111001110100010'

# Define your timing values
# Ces valeur marche pour partir la generatrice

TRANSMIT_PIN = 18           # GPIO pin for transmitting
NUM_ATTEMPTS = 10            # Number of attempts to send the code
short_delay = 352           # Short pulse duration (in µs)
long_delay = 1067           # Long pulse duration (in µs)
extended_delay = 11812       # Extended delay (in µs)


def precise_sleep(delay_us):
    """Busy-wait sleep for precise microsecond delays"""
    start_ns = time.monotonic_ns()
    target_ns = start_ns + (delay_us * 1_000)
    while time.monotonic_ns() < target_ns:
        pass

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter with timing debug'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    print("\n🚀 Starting transmission...")

    for t in range(NUM_ATTEMPTS):
        print(f"\n🔹 Attempt {t + 1}/{NUM_ATTEMPTS}")
        
        for i, bit in enumerate(code):
            print(f"  ➡️ Transmitting bit {i + 1}/{len(code)}: {bit}")

            start_time = time.monotonic_ns()

            if bit == '0':
                # '0': Short ON + Long OFF
                GPIO.output(TRANSMIT_PIN, 1)
                precise_sleep(short_delay)     # Use precise sleep
                GPIO.output(TRANSMIT_PIN, 0)
                precise_sleep(long_delay)

            elif bit == '1':
                # '1': Long ON + Short OFF
                GPIO.output(TRANSMIT_PIN, 1)
                precise_sleep(long_delay)      # Use precise sleep
                GPIO.output(TRANSMIT_PIN, 0)
                precise_sleep(short_delay)

            else:
                #print(f"    ⚠️ Invalid bit: {bit}, skipping...")
                continue

            # Measure actual elapsed time
            end_time = time.monotonic_ns()
            elapsed_us = (end_time - start_time) / 1_000  # Convert to microseconds
            print(f"    ⏱️ Actual elapsed time: {elapsed_us:.0f} µs")

        # Add extended delay between transmission attempts
        print(f"  ⏸️", end="")
        precise_sleep(extended_delay)
    GPIO.output(TRANSMIT_PIN, 0)
    GPIO.cleanup()
    print("\n✅ Transmission complete.")

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
