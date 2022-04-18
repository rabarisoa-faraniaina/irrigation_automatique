import csv

def sensors_data_to_csv(data_to_write):
    # data_header = ['Date and time','temperature','humidity']

    with open('exports/csv/sensorsData.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            lastline = row

        if lastline[0] != data_to_write[0]:
            with open('exports/csv/sensorsData.csv', 'a', newline='') as csvfile:
                # create a csv dictionary writer and add data header
                csvwriter = csv.writer(csvfile)
                # writer.writerow()
                csvwriter.writerow(data_to_write)
                print("INFO: sensors data saved to csv")
        else:
            print("WARNING: no new measure from Arduino sensors")

def forecast_data_to_csv(data_to_write):
    # data_header = ['Measure Date and time','numberHoursLater,'temperatureForecast','humidityForecast','rainForecast']

    with open('exports/csv/forecastData.csv', newline='') as f:
        reader = csv.reader(f)
        # lastline = reader.keys()[-1]
        for row in reader:
            lastline = row

        if lastline[0] != data_to_write[0]:
            with open('exports/csv/forecastData.csv', 'a', newline='') as csvfile:
                # create a csv dictionary writer and add data header
                csvwriter = csv.writer(csvfile)
                # writer.writerow()
                csvwriter.writerow(data_to_write)
                print("INFO: forecast data saved to csv")
        else:
            print("WARNING: no new measure from MeteoAPI")
