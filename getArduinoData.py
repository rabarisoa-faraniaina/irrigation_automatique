import serial, schedule

list_values = []
list_in_floats = []

def getDataFromArduino():
    arduino = serial.Serial('com3',115200)
    arduino_data = arduino.readline()

    decoded_data = str(arduino_data[0:len(arduino_data)].decode('utf-8'))
    list_values = decoded_data.split('x')

    for item in list_values:
        list_in_floats.append(str(item))

    print("Data collected: "+ str(list_in_floats))

    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    arduino.close()