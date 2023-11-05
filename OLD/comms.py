import serial
import time

# Init UART on COM Port 3
arduino = serial.Serial(port='COM4',  baudrate=115200, timeout=.1)

#timer = 0

# Read Comms Data
def checkTrigger():
    global timer
    val = arduino.readline().decode()
    if(val == "T"):
        #timer = round(time.time() * 1000)
        return True
    elif(val == "F"):
        #print(round(time.time() * 1000) - timer)
        print("Fired")

    return False

# Main Loop
while True:
    if(checkTrigger()):
        arduino.write(bytes("D",  'utf-8'))
        print("Trigger Detected")