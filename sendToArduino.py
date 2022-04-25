import serial

def sendBytes(value):
    arduino = serial.Serial('com3',115200)
    arduino.write('result')
    arduino.write(bytes(value,'utf-8'))
