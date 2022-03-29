import serial, schedule
from datetime import datetime,time
import pyfirmata
import re
import requests
import export

list_values = []
list_in_floats = []
res = False

def getDataFromArduino():
    arduino = serial.Serial('com3',115200)
    print('get here')
    #send data to arduino
    res = False
    arduino.write(bytes(res))
    arduino_data = arduino.readline()

    decoded_data = str(arduino_data[0:len(arduino_data)].decode('utf-8'))
    list_values = decoded_data.split('x')

    #get current date and time
    now = datetime.now()
    date_formatted = now.strftime("%d/%m/%Y %H:%M:%S")
    
    for item in list_values:
        print('eto')
        print(item)
        value = re.findall(r"[-+]?\d*\.*\d+",item)
        if( len(value) != 0):
            list_in_floats = [{'date':date_formatted,'temperature':value[0], "humidity":value[1]}]
            #list_in_floats.append(date_formatted+':'+str(item))
            printed_value = [{'date':date_formatted,'temperature':value[0], "humidity":value[1]}]
            exported_value = [date_formatted,value[0],value[1]]
            temp = value[0]
            hum = value[1]
            export.to_csv(exported_value)
            print("Data collected: "+ str(printed_value))
        print("Data collected: "+ str(list_in_floats))
    
    #store into database
    requests.post('http://192.168.1.25:5001/receive/temp/hum')
    #requests.post('http://192.168.1.25:5001/send/0')
    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    arduino.close()

#seconde methode
def fct():
    port = 'COM3'
    HIGH = True
    LOW = False

    board = pyfirmata.Arduino(port)
    temp_pin = board.get_pin('a:1:i')
    iterator = pyfirmata.util.Iterator(board)
    hum_pin = board.get_pin('a:2:i')
    try:
        while True:
            print('ici')
            print('Temperature: ',temp_pin.read())
            print('humidity:',hum_pin.read())
    except:
        #time.sleep(2)
        board.exit()