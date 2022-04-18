import time
import ubidotsAPI
import schedule
import meteoAPI

# -------------- MAIN PROGRAM -----------------

NUMBER_OF_MINUTES = 0.1

def newAnalysis():
    print("\n---------------------------- NEW ANALYSIS",
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