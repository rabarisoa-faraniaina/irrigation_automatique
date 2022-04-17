import requests
import time

# -------------- GET DATA FROM ARDUINO -----------------

# Assign your Ubidots Token
TOKEN = "BBFF-vV3g09kNJipYFlzmmuSzt34aTckMDv"
# Assign the device label to obtain the variable
DEVICE = "eui-lora"
# Assign the variable label to obtain the variable value
HUMIDITY = "humidity"
TEMPERATURE = "temperature"
DELAY = 10  # Delay in seconds

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


# -------------- GET DATA FROM METEO -----------------



# -------------- MAIN PROGRAM -----------------

if __name__ == "__main__":
    while True:
        print("Humidity : ", getSensorsData(DEVICE, HUMIDITY))
        print("Temperature : ", getSensorsData(DEVICE, TEMPERATURE))
        time.sleep(DELAY)


