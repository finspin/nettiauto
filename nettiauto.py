#!/usr/bin/env python

import scraper
import spreadsheet
import smtplib
import sys
import config

def scrape_data():
    '''Scrape nettiauto.com for the car IDs that are
    stored in Google spreadsheet and return scraped
    data
    '''

    gspreadsheet = spreadsheet.Spreadsheet()
    nscraper = scraper.Scraper()

    car_ids = gspreadsheet.get_car_ids() 
    return nscraper.get_data(car_ids)

def update_worksheet():
    data = scrape_data()
    gspreadsheet = spreadsheet.Spreadsheet()
    gspreadsheet.update(data)

def mail_price_changes():
    gss = spreadsheet.Spreadsheet()
    gspreadsheet = gss.open()
    last_row = len(gspreadsheet.col_values(1))
    second_last_row = last_row - 1
    last_row_values = gspreadsheet.row_values(last_row)[1:]
    second_last_row_values = gspreadsheet.row_values(second_last_row)[1:]

    for i, new_price in enumerate(last_row_values):
        car_name = gspreadsheet.cell(2, i + 2).value
        car_link = gspreadsheet.cell(5, i + 2).value
        old_price = second_last_row_values[i]
        if new_price < old_price:
            fromaddr = config.email
            toaddrs  = config.email
            subject = "Subject: Nettiauto - %s price dropped: %s --> %s\n\n" % (car_name, old_price, new_price)
            msg = "Car link: %s" % car_link
            
            username = config.connection['username']
            password = config.connection['password']
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, subject + msg)
            server.quit()

if __name__ == "__main__":
    update_worksheet()
    mail_price_changes()
