import serial
#import time
#from threading import Thread

# Init UART on COM Port 3
arduino = serial.Serial(port='COM3',  baudrate=115200, timeout=.1)

#arduino.write(bytes(x,  'utf-8'))

# Read Comms Data
def checkTrigger():
    if(arduino.readline().decode() == "Trigger"):
        return True
    return False

# Main Loop
while True:
    if(checkTrigger()):
        print("Trigger Detected")