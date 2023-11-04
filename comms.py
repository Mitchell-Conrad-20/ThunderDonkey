import serial
#import time
from threading import Thread

# Init UART on COM Port 3
arduino = serial.Serial(port='COM3',  baudrate=115200, timeout=.1)

#arduino.write(bytes(x,  'utf-8'))

# Read Comms Data
def checkTrigger():
    while True:
        if(arduino.readline().decode() == "Trigger"):
            print("Trigger Detected")



if __name__ == "__main__":
    # Setup
    triggerThread = Thread(target=checkTrigger, daemon=True)
    triggerThread.start

    # Main Loop
    while True:
        pass