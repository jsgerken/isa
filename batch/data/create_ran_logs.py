import csv
from random import randint
with open('viewLogs.csv', 'a') as logfile:
    csvwriter = csv.writer(logfile)
    for i in range(300):
        csvwriter.writerow([randint(1, 100), randint(1, 14)])
