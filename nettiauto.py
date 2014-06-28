# TODO: ERROR HANDLING
import requests
from BeautifulSoup import BeautifulSoup
import gspread
import datetime
import time
from random import randrange
import json
import sys

today = datetime.date.today()

# Load configuration file    
config = json.loads(open('config.json').read())

# Login with your Google account
gc = gspread.login(config['username'], config['password'])

# Open a worksheet from spreadsheet
wks = gc.open(config['spreadsheet']).sheet1

# Get cars URLs from spreadsheet
cars = wks.row_values(1)[1:]

# Get next empty row and insert current date
urow = len(wks.col_values(1)) + 1
wks.update_cell(urow, 1, str(today))

# Insert price for each car
for i, car in enumerate(cars):
    time.sleep(randrange(2, 5))
    r = requests.get(car)
    soup = BeautifulSoup(r.content)

    make = car.split('/')[-3].title()
    model = car.split('/')[-2].title()
    year = soup.find('div', id="id_adInfo").table.findAll('tr')[0].findAll('td')[1].text[:4]
    mileage = soup.find('div', id="id_adInfo").table.find(text="Mittarilukema").parent.findNext('td').text
    price = soup.find('span', itemprop="price").text
    price = filter(lambda x: x.isdigit(), price)

    # Insert car name, year and mileage if empty
    # This is for newly added cars
    if wks.cell(2, i + 2).value == '':
        wks.update_cell(2, i + 2, make + " " + model)
    if wks.cell(3, i + 2).value == '':
        wks.update_cell(3, i + 2, year)
    if wks.cell(4, i + 2).value == '':
        wks.update_cell(4, i + 2,  mileage)

    wks.update_cell(urow, i + 2, price)

