import requests, json

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


def getWHourlyForcast():
    CITY = "Avignon"
    #base url
    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"

    data = getLonLat(CITY)
    lat = str(data[0]['lat'])
    lon = str(data[0]['lon'])
    print('Latitude: '+ lat)
    print('Longiture: '+ lon)
    #updating url
    URL = BASE_URL + "lat="+ lat +"&lon="+ lon + "&units=metric&exclude=alerts,current,minutely,daily&appid=" + API_KEY
    #HTTP REQUEST
    response = requests.get(URL)

    if response.status_code == 200:
        res = response.json()
        return res
    else:
        print("Error in the HTTP request")

#daily forecast
def getDailyForcast():
    print('Bonjoour')