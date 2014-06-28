#!/usr/bin/env python

import requests
import logging
import time
from BeautifulSoup import BeautifulSoup
from random import randrange


class Scraper:
    '''Scraper scrapes data from http://nettiauto.com website
    and provides it to other modules.
    '''

    def __init__(self):
        self._base_url = 'http://www.nettiauto.com/'

    def get_data(self, car_ids):
        '''Loop through car IDs, scrape and return data.
        '''

        self._car_ids = car_ids
        self._data = {} 

        for i, car_id in enumerate(self._car_ids):

            # Wait a few seconds between each server request
            time.sleep(randrange(2, 5))
            url = self._base_url + car_id
            self._data[car_id] = {} 

            try:
                # Request to base_url + id which is redirected
                # to base_url/make/model/id
                r = requests.get(url)
            except requests.exceptions.RequestException as e:
                self._data[car_id]['status'] = 'Connection problems'
                logging.exception(e)
                break
            
            if r.status_code == 200:
                soup = BeautifulSoup(r.content)

                try:
                    url = soup.find('meta', property='og:url')['content']
                except:
                    url = 'N/A'

                if url != 'N/A':
                    make = url.split('/')[-3].title()
                    model = url.split('/')[-2].title()
                else:
                    make = 'N/A'
                    model = 'N/A'

                try:
                    year = soup.find('div', id="id_adInfo").table.findAll('tr')[0].findAll('td')[1].text[:4]
                except:
                    year = 'N/A'
                try:
                    mileage = soup.find('div', id="id_adInfo").table.find(text="Mittarilukema").parent.findNext('td').text
                except:
                    mileage = 'N/A'
                try:
                    price = soup.find('span', itemprop="price").text 
                    price = filter(lambda x: x.isdigit(), price)
                except:
                    price = 'Car sold!'

                    # price = soup.find('span', itemprop="price") 
                    # price = filter(lambda x: x.isdigit(), price.text) if price is not None else 'Car sold!'
                self._data[car_id]['status'] = 'OK' 
                self._data[car_id]['url'] = url
                self._data[car_id]['make'] = make 
                self._data[car_id]['model'] = model 
                self._data[car_id]['year'] = year 
                self._data[car_id]['mileage'] = mileage 
                self._data[car_id]['price'] = price 
            else:
                self._data[car_id]['status'] = 'Couldn\'t fetch data'

        return self._data
