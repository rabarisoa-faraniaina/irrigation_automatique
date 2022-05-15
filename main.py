import time
import ubidotsAPI
import schedule
import MeteoAPI
import manageValveAI
from datetime import datetime

# -------------- MAIN PROGRAM -----------------

NUMBER_OF_MINUTES = 0.1

def newAnalysis():
    # get current date and time
    now = datetime.now()
    date_formatted = now.strftime("%d/%m/%Y %H:%M:%S")

    print("\n------------------------ NEW ANALYSIS",
                                date_formatted,
                                 "(every", NUMBER_OF_MINUTES, "min) -----------------------------")
    # get data from arduino every hour
    sensorsData = ubidotsAPI.getData()

    # get data from meteo every hour
    meteoData = MeteoAPI.getData()


    # analyse data to open or close electrovanne

    altidud = 23  # Avignon /** take from weatherAPI*/
    dataa = MeteoAPI.getLonLat("Avignon")
    
    
    #phi = 43.9493  # lattitude Avignon 
    # take from weatherAPI
    phi = int(dataa[0]['lat']) 
    soilType = 3   # Argileux (peu drainant)
    fieldArea = 10000  # field area(m2)

    soilHumidity = sensorsData[1]
    soilTemperature = sensorsData[2]

    airHumidity = meteoData[0]
    airTemperature = meteoData[1]
    rain = meteoData[2]
    windSpeed = meteoData[3]

    manageValveAI.manageValve(altidud, phi, soilType, soilHumidity, soilTemperature, airHumidity, airTemperature, rain, windSpeed, fieldArea)

def run():
    print("Program running ...")
    schedule.every(NUMBER_OF_MINUTES).minutes.do(newAnalysis)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()