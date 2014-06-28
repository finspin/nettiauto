#!/usr/bin/env python

import gspread
import datetime
import sys
import logging
import config

today = datetime.date.today()


class Spreadsheet:

    def __init__(self):
        self._username = config.connection['username'] 
        self._password = config.connection['password'] 
        self._spreadsheet = config.connection['spreadsheet']
        self._email = config.email

    def get_car_ids(self):
        '''Returns a list of cars' IDs which need to be updated
        '''

        self._worksheet = self.open() 
        self._car_ids = self._worksheet.row_values(1)[1:]
        return self._car_ids
 
    def open(self):
        '''Opens a spreadsheet, returning a Spreadsheet instance.
        If opening a spreadhseet fails, program exits.
        '''

        try:
            glogin = gspread.login(self._username, self._password)
        except Exception as e:
            logging.exception(e)
            sys.exit(1)
        try:
            worksheet = glogin.open(self._spreadsheet).sheet1
            return worksheet 
        except Exception as e:
            logging.exception(e)
            sys.exit('Spreadsheet doesn\'n exist.')

    def construct_worksheet(self):
        '''Fill in the column A if empty.
        Fills in values like Car Name, Year, Mileage, URL.
        Values are filled only if it's first time that
        worksheet is updated.
        '''

        self._worksheet = self.open() 

        # Fill the A column if empty
        if self._worksheet.cell(2, 1).value == '':
            self._worksheet.update_cell(2, 1, 'Car Name')
        if self._worksheet.cell(3, 1).value == '':
            self._worksheet.update_cell(3, 1, 'Year')
        if self._worksheet.cell(4, 1).value == '':
            self._worksheet.update_cell(4, 1, 'Mileage')
        if self._worksheet.cell(5, 1).value == '':
            self._worksheet.update_cell(5, 1, 'URL')
        if self._worksheet.cell(6, 1).value == '':
            self._worksheet.update_cell(6, 1, 'Status')

    def update(self, data):

        self._worksheet = self.open() 
        self._data = data
        self._car_ids = self.get_car_ids()

        # Get next empty row and insert current date
        try:
            price_row = len(self._worksheet.col_values(1)) + 1
            self._worksheet.update_cell(price_row, 1, str(today))
        except Exception as e:
            logging.exception(e)
            sys.exit(1)

        for car_id in self._car_ids:
            column = self._worksheet.find(car_id).col 
            # Insert car name, year, mileage and url if empty
            # This is for newly added cars
            try:
                if self._worksheet.cell(2, column).value == '':
                    self._worksheet.update_cell(2, column, self._data[car_id]['make'] + " " + self._data[car_id]['model'])
                if self._worksheet.cell(3, column).value == '':
                    self._worksheet.update_cell(3, column, self._data[car_id]['year'])
                if self._worksheet.cell(4, column).value == '':
                    self._worksheet.update_cell(4, column,  self._data[car_id]['mileage'])
                if self._worksheet.cell(5, column).value == '':
                    self._worksheet.update_cell(5, column,  self._data[car_id]['url'])
                self._worksheet.update_cell(6, column,  self._data[car_id]['status'])

                # Insert price for today
                self._worksheet.update_cell(price_row, column, self._data[car_id]['price'])
            except KeyError as e:
                self._worksheet.update_cell(6, column,  'Not scraped')
