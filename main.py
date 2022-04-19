import time
import ubidotsAPI
import schedule
import meteoAPI
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
    ubidotsAPI.getData()

    # get data from meteo every hour
    meteoAPI.getData()

    # todo analyse data to open or close electrovanne


def run():
    print("Program running ...")
    schedule.every(NUMBER_OF_MINUTES).minutes.do(newAnalysis)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()