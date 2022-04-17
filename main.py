import time
import meteo
# import getArduinoData
import schedule

def run():
    print("Program started")
    response = meteo.usePyown()
    # meteo.displayResults(response)
    # print("Hourly : "+ str(response['hourly']))
    schedule.every(10).seconds.do(meteo.usePyown)
    #schedule.every(10).seconds.do(getArduinoData.getDataFromArduino())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()