import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import urllib


def scrapper():

    # url = "https://www.lib.berkeley.edu/libraries/moffitt-library"
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    url = "https://www.lib.berkeley.edu/hours/api/libraries/179?begin_date=2019-11-10&end_date=2019-11-16"
    data = json.load(urllib.request.urlopen(url))
    #page = requests.get(url)
    #test = page.content[0]
    start_time = data[0]["hours"][0]["day"]["start"]

if __name__ == "__main__":
    scrapper()