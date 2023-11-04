import serial
import time
#from threading import Thread

# Init UART on COM Port 3
arduino = serial.Serial(port='COM3',  baudrate=115200, timeout=.1)

#arduino.write(bytes(x,  'utf-8'))

timer = 0

# Read Comms Data
def checkTrigger():
    global timer
    val = arduino.readline().decode()
    if(val == "T"):
        timer = round(time.time() * 1000)
        return True
    elif(val == "F"):
        print(round(time.time() * 1000) - timer)
        #print("Fired")

    return False

# Main Loop
while True:
    if(checkTrigger()):
        arduino.write(bytes("D",  'utf-8'))
        print("Trigger Detected")