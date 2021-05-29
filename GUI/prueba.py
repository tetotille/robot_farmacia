# Importing Libraries
import serial
import time
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.5)
    while True:
        data = arduino.readline().decode()
        print(data)
        time.sleep(0.5)
    return data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value
    print(arduino.read().decode())
