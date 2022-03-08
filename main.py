import time
import meteo
import getArduinoData
import schedule


def run():
    response = meteo.getWHourlyForcast()
    #print("Hourly : "+ str(response['hourly']))
    print("Program started")
    schedule.every(10).seconds.do(getArduinoData.getDataFromArduino)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()