import requests, json
from pyowm.owm import OWM

#api key
API_KEY = "45548940d7e519425e0ad75bc67bce50"

#get latitude and longitude 
def getLonLat(CITY):

    BASE_URL = "http://api.openweathermap.org/geo/1.0/direct?"

    #updating url
    URL = BASE_URL + "q="+ CITY +"&limit=1&appid=" + API_KEY
    #HTTP REQUEST
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        return data

#get the temperature and humidity in three hours
def usePyown():
    CITY = 'Avignon'
    owm = OWM("45548940d7e519425e0ad75bc67bce50")
    mgr = owm.weather_manager()
    data = getLonLat(CITY)
    lat = int(data[0]['lat'])
    lon = int(data[0]['lon'])
    # what is the epoch for 3 days later at this time?
    one_call = mgr.one_call(lat=int(lat), lon=int(lon))
    temp = one_call.forecast_hourly[3].temperature('celsius').get('temp',None)
    hum = one_call.forecast_hourly[3].humidity
    print("Temperature: ",temp)
    print("Humidity: ",hum)
