DRAFT DRAFT 🛠️ Raspberry Pi 433 MHz Generator Control
A project to control the Westinghouse WGEN3600DFc generator using a 433 MHz remote key fob and a Raspberry Pi.

🚀 Project Overview
This project uses a 433 MHz RF transmitter connected to a Raspberry Pi to simulate the signals sent by the Westinghouse 100714A remote key fob. The goal is to remotely start and stop the generator using custom scripts.

🔧 Hardware
✅ Raspberry Pi
✅ 433 MHz RF transmitter
✅ Westinghouse 100714A remote key fob
FCC ID: RKWTX0201
Based on the EV1527 encoder
✅ Jumper wires and breadboard (for prototyping)
📚 References and Inspiration
Super Simple Raspberry Pi 433MHz Home Automation
RF 433 MHz Raspberry Pi
EV1527 Encoder Datasheet: EV1527.pdf
GitHub Repository (attempted but not used):
milaq/rpi-rf
rpi-rf on PyPi
🛠️ Setup Instructions
Create a Python Virtual Environment

bash
Copy
Edit
sudo apt update
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
Install Required Libraries

bash
Copy
Edit
pip install rpi-rf
pip install gpiozero
Wiring

Connect the RF transmitter to the Pi's GPIO pins:
VCC → 3.3V
GND → Ground
DATA → GPIO17 (or your chosen pin)
Signal Capture

Use xxxxxxxxxxx to capture the remote’s signal and identify the ON/OFF codes.
Script Execution

Use a Python script to send the ON/OFF signal to the generator.
⚙️ Usage
Run the script to remotely start or stop the generator:

bash
Copy
Edit
python control_generator.py --action on
python control_generator.py --action off

✅ Troubleshooting
If you encounter issues:

Double-check the GPIO wiring.
Ensure the RF transmitter uses the correct voltage.
Verify the captured codes using rpi-rf_receive.
📌 To-Do
Add automation scripts for scheduled generator control.
Integrate with a home automation system (e.g., Home Assistant).
