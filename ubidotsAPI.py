import requests
import exportCSV
from datetime import datetime


# -------------- GET DATA FROM ARDUINO -----------------

# Assign your Ubidots Token
TOKEN = "BBFF-vV3g09kNJipYFlzmmuSzt34aTckMDv"
# Assign the device label to obtain the variable
DEVICE = "eui-lora"
# Assign the variable label to obtain the variable value
MOISTURE_KEY = "humidity"
TEMPERATURE_KEY = "temperature"
global moistureValue
global temperatureValue

def getLastMeasureDate(device, variable):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
              "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['timestamp']
    except:
        pass

def getSensorsData(device, variable):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
              "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass


def getData():
    lastMeasureDatetime = datetime.fromtimestamp(getLastMeasureDate(DEVICE, MOISTURE_KEY)/1000)
    lastMeasureDatetime = lastMeasureDatetime.strftime("%d/%m/%Y %H:%M:%S")
    moistureValue = getSensorsData(DEVICE, MOISTURE_KEY)
    temperatureValue = getSensorsData(DEVICE, TEMPERATURE_KEY)/100

    # get current date and time
    # now = datetime.now()
    # date_formatted = now.strftime("%d/%m/%Y %H:%M:%S")

    # save data to csv
    print("Sensors data - ", lastMeasureDatetime, " => Humidity:", moistureValue, ", Temperature:", temperatureValue)
    data_to_save = [lastMeasureDatetime, temperatureValue, moistureValue]
    exportCSV.sensors_data_to_csv(data_to_save)
