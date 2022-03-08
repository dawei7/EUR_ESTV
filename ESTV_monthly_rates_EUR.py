# Monthly ESTV rates is a public Get Request without identification
#
# Base URL for average monthly rates in CHF/EUR -> 42 is for currency Euro
# https://www.backend-rates.bazg.admin.ch/api/xmlavgyear/42
# 
# Parameters:
# e.g. j = 2021
# e.g. locale = en
# Query -> 42 is Euro import request
#
#Example for 2021 # https://www.backend-rates.bazg.admin.ch/api/xmlavgyear/42?j=2021&locale=en


import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

years = [2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030]
language = "en"

my_table = [["year","month","monthlyAvgRate"]]

my_dict={
    "January":'01',
    "February":'02',
    "March":'03',
    "April":'04',
    "May":'05',
    "June":'06',
    "July":'07',
    "August":'08',
    "September":'09',
    "October":'10',
    "November":'11',
    "December":'12'
}



for year in years:

    params = {
    "j":year,
    "locale":language
    }

    soup_EUR = BeautifulSoup(requests.get("https://www.backend-rates.bazg.admin.ch/api/xmlavgyear/42",params=params).content, 'html.parser')

    avgrates_EUR = soup_EUR.findAll('avgrate')


    for i in range(len(avgrates_EUR)):

        my_table.append([year,my_dict[avgrates_EUR[i].parent.find("month").text],round(float(avgrates_EUR[i].text),4)])
    
#print(*my_table,sep="\n")

# CSV
with open('EUR_RATES.csv', 'w', encoding='UTF8',newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    for row in my_table:
        writer.writerow(row)

# Pandas
df = pd.DataFrame(my_table)

# First row as header
df.columns = df.iloc[0]
df = df[1:]


print(df)