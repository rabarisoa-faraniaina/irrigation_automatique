import csv

def to_csv(data_from_ard):
    data_header = ['Date and time','temperature','humidity']

    with open('exports/csv/data.csv','a',newline='') as csvfile:
        #create a csv dictionary writer and add data header
        csvwriter = csv.writer(csvfile)
        #writer.writerow()
        csvwriter.writerow(data_from_ard)