import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.001)

def write_to_arduino(message):
   try:
      arduino.write(bytes(message, 'utf-8'))
      return True
   except:
      print("Serial communication error!")
      return False

def read_from_arduino():
   try:
      data = arduino.readline()
      if len(data) > 0:
         return data
      else:
         return None
   except:
      print("Read error!")
      return None


while True:
   data = read_from_arduino()
   # initilize the serial comms
   write_to_arduino("66")
   write_to_arduino("66")
   write_to_arduino("66")
   write_to_arduino("66")
   if data is not None:
      print(data)
   else:
      num = input("Enter 6 for death: ") # Taking input from user
      initial = time.time()
      write_to_arduino(num)
      value = read_from_arduino()
      fps = time.time() - initial
      if fps > 0:
         fps = int(1/fps)
      print(f"FPS:{fps}")
      print(value) # printing the value


# Steps:
# - Trigger pull -> arduino confirm to python (send 330)
# - Python confirms sends (send 440) or denies (550)
#    - python also sends gun type
#
# - If death python contacts arduino

# Codes
 #Arduino:
#  - 1 = ask for shot confirm
# Python:
# - 3 = no shot, 4-(5or6) = shot confirmed
# - 44 = death
# - 5 is ar 6 is pistol or smg