# 🛠️ **Raspberry Pi 433 MHz Generator Control**
A project to control the **Westinghouse WGEN3600DFc (or any WGEN with auto start) generator** using a **433 MHz remote key fob** and a **Raspberry Pi**.

I'm not a coder by profession but this works, tried to document the best I could my experience.  It took a few days before I could get the timing right because of internal latency on the RPI, once I adjusted sleep timers to match the expected FR322 protocol, it all started to work.  Getting the FOB to play right next to the receiver was a big plus.

Using my RPI I can monitor the status of my batteries, and during the winter time, then snow covers the solar panels, I can remotely start the 

## 🚀 **Project Overview**
This project utilizes a **433 MHz RF transmitter** connected to a Raspberry Pi to simulate the signals sent by the **Westinghouse 100714A remote key fob**. The goal is to remotely start and stop the generator using custom scripts, enhancing home energy resilience during power outages or for scheduled maintenance. The remote uses **Manchester encoding**, a method to encode the clock and data of a synchronous bit stream.


## 🔧 **Hardware**
- ✅ **Westinghouse WGEN3600DFc (or any WGEN with auto start) generator** 
- ✅ **Raspberry Pi** 
- ✅ **433 MHz RF transmitter**
- ✅ **Westinghouse 100714A remote key fob**
  - FCC ID: RKWTX0201
  - Based on the **EV1527 encoder**
- ✅ Jumper wires and breadboard (for prototyping)

## 📚 **References and Inspiration - not repeating what they wrote **
- [Super Simple Raspberry Pi 433MHz Home Automation](https://www.instructables.com/Super-Simple-Raspberry-Pi-433MHz-Home-Automation/)
- [RF 433 MHz Raspberry Pi](https://www.instructables.com/RF-433-MHZ-Raspberry-Pi/)
- **EV1527 Encoder Datasheet:** [EV1527.pdf](https://www.sunrom.com/download/EV1527.pdf)
- **GitHub Repository (attempted but not used):**
  - [milaq/rpi-rf](https://github.com/milaq/rpi-rf)
  - [rpi-rf on PyPi](https://pypi.org/project/rpi-rf/)

## 🛠️ **Setup Instructions**
1. **Create a Python Virtual Environment**

   - This is new to me, so took a while to get going. At a high level this is the steps.
   
   ```bash
   sudo apt update
   sudo apt install python3-venv
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Required Libraries**
   ```bash
   pip install rpi-rf
   pip install gpiozero
   + other? forgot to track... 
   ```

3. **Wiring**
   - Connect the **RF transmitter** to the Pi's GPIO pins:
     - **VCC** → 5V
     - **GND** → Ground
     - **DATA** → GPIO17 (or your chosen pin)
	Connect the **RF receiver** to the Pi's GPIO pins:
     - **VCC** → 5V
     - **GND** → Ground
     - **DATA** → GPIO12 (or your chosen pin)
	** I soldered an antenna 173mm (6"7/8) to both receiver and transmitter, signal was much cleaner.

4. **Step 1 - Signal Capture**
   - Use `1-collect-signal.py` to capture the remote’s signal and identify the ON/OFF codes.
	- keep the fob start button pressed before and after the test, keep it close to the receiver
	- later, repeat for the stop button
	- the signal is manchester encoded, to the raw date needs to be processed and parsed

## 📊 **Raw data: (example) (`rf_signal_data.txt`)**


Time (µs), Signal
159, 0  <- at this time the signal was a 0.  My RPI can scan at about 20 to 30 microsecond sample rate.
231, 0
262, 0
296, 0
322, 1
347, 1

5. **Step 2 - Process the captured signal **
   - Use `2-process-signal.py`  Python script to process the captured file.


## 📊 **Understanding the Parsed Signal Data (`parsed_rf_signal.txt`)**

The `parsed_rf_signal.txt` file contains the processed output from the captured 433 MHz signal. Each line represents a distinct pulse and its duration or pause in the signal, described by two values:

* **Signal (0 or 1):**
    * `0` indicates a low signal (OFF).
    * `1` indicates a high signal (ON).
* **Duration (µs):**
    * The duration of the signal state in microseconds.

Here's an example from the file:
Signal, Duration (µs)
1, 344   <- this is a 0  (short 1 and long 0)
0, 1131
1, 362   <- 0
0, 1120
1, 1130  <- this is a 1 (long 1 and short 0)
0, 388
1, 1110  <- 1
0, 387
1, 1120  <- 1
0, 382
1, 328   <- 0
0, 1156
1, 344   < preamble? >
0, 11804 <- pause between sequences

6. **Step 3 - Parse the captured signal file**
   - Use `3-parse-rf-signal.py`  Python script to parse the processed file to find the sequence and codes.
   - The output provides a list of codes, hopefully they will work in the transmit.

## 📊 **Understanding the output of the Parsed Signal Data**

$ python 3-parse-rf-signal.py

🔹 Step 1: Reading file...
✅ Loaded 527 signal entries

🔹 Step 2: Processing signal pairs...

🔹 Final Decoded Sequences:
111000000111001110100001 - 24  <- this is the code for the generator, unique or not, don't know if the use all the same code.
111000000111001110100001 - 24
111000000111001110100001 - 24
111000000111001110100001 - 24
111000000111001110100001 - 24
111000000111001110100001 - 24
111000000111001110100001 - 24
111000000111001110100001 - 24
111000000111001110100001 - 24


7. **Step 4 - Transmit the discovered code**
   - Repeat step 1, 2 and 3 for the stop code.  Update the script with the start and stop code. 
   - Use `4-transmit.py start or stop`  To send the code via RF433 to the generator, hopefully it will work.
   - If not, you need to adjust the timing of the signals, the low, the high, un microseconds, your RPI may be faster or slower than mine (3B)
   - Note: there's no relation I can see between the ID sticker on the fob and the discovered code.

## ✅ **Timing is everything - precise sleep **

This took a while, either my RPI is too slow, but I time.sleep() didn't cut it, had to use a precision sleep and it worked.

$ python 4-transmit.py  stop

🚀 Starting transmission...

🔹 Attempt 1/10
  ➡️ Transmitting bit 1/24: 1
    ⏱️ Actual elapsed time: 1566 µs
  ➡️ Transmitting bit 2/24: 1
    ⏱️ Actual elapsed time: 1567 µs
  ➡️ Transmitting bit 3/24: 1
    ⏱️ Actual elapsed time: 1517 µs
  ➡️ Transmitting bit 4/24: 0
    ⏱️ Actual elapsed time: 1510 µs
  ➡️ Transmitting bit 5/24: 0
    ⏱️ Actual elapsed time: 1498 µs
  ➡️ Transmitting bit 6/24: 0
    ⏱️ Actual elapsed time: 1490 µs

NOTE: the actual time is what you need to adjust to make sure the timing of the signal is what the receiver is expecting.

	- short_delay = 352           # Short pulse duration (in µs)
	- long_delay = 1067           # Long pulse duration (in µs)
	- extended_delay = 11812      # Extended delay (in µs)


## ✅ **Troubleshooting**
If you encounter issues:
- Double-check the GPIO wiring.
- Ensure the RF transmitter uses the correct voltage.
- Verify the captured codes.
- Ensure good ground, good power supply.

## 📌 **To-Do**
- Add automation scripts for scheduled generator control.
- Integrate with a home automation system (e.g., Home Assistant).

