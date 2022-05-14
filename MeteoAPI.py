import requests, json
from pyowm.owm import OWM
import exportCSV
from datetime import datetime

# -------------- GET DATA FROM METEO -----------------


# api key
API_KEY = "45548940d7e519425e0ad75bc67bce50"
CITY = 'Avignon'
HOURS_LATER = 24
global forecastTemperature
global forecastHumidity
global forecastRain


# get latitude and longitude
def getLonLat(CITY):
    BASE_URL = "http://api.openweathermap.org/geo/1.0/direct?"

    # updating url
    URL = BASE_URL + "q=" + CITY + "&limit=1&appid=" + API_KEY
    # HTTP REQUEST
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        return data


# get the temperature and humidity in three hours
def getData():
    owm = OWM("45548940d7e519425e0ad75bc67bce50")
    mgr = owm.weather_manager()
    data = getLonLat(CITY)
    lat = int(data[0]['lat'])
    lon = int(data[0]['lon'])
    # what is the epoch for 3 hours later at this time?
    one_call = mgr.one_call(lat=int(lat), lon=int(lon))
    forecastTemperature = one_call.forecast_hourly[HOURS_LATER].temperature('celsius').get('temp')
    forecastAirHumidity = one_call.forecast_hourly[HOURS_LATER].humidity
    forecastAirHumidity = forecastAirHumidity/100
    forecastRain = one_call.forecast_hourly[HOURS_LATER].rain.get('1h')
    if forecastRain is None:
        forecastRain = 0
    forecastWindSpeed = one_call.forecast_hourly[HOURS_LATER].wnd.get('speed')

    # get current date and time
    now = datetime.now()
    date_formatted = now.strftime("%d/%m/%Y %H:%M:%S")

    # save data to csv
    print("MeteoForecast -", HOURS_LATER, "h later => ",
          "AirHumidity:", forecastAirHumidity,
          ", Temperature:", forecastTemperature,
          ", Rain:", forecastRain,
          ", WindSpeed:", forecastWindSpeed)
    data_to_save = [date_formatted, HOURS_LATER, forecastTemperature, forecastAirHumidity, forecastRain,
                    forecastWindSpeed]
    exportCSV.forecast_data_to_csv(data_to_save)
    return [forecastAirHumidity, forecastTemperature, forecastRain, forecastWindSpeed];
