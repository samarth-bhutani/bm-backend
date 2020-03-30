import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import helper
import re


def rsf_scrapper():
    open_close_array = []
    output_dictionary = {}

    url_rsf = "https://recsports.berkeley.edu/rsf-hours/"
    

    page = requests.get(url_rsf)
    soup = BeautifulSoup(page.content,"html.parser")
    content = soup.find(class_="minimal_table")
    content_iterable = content.findAll("tr")
   
    
    for i in content_iterable:
        day_iterable = i.findAll("td")
        day = str(datetime.strptime(str(day_iterable[0].get_text().replace(",","")), '%a %b %d')).replace("1900",str(datetime.now().year)).split(" ")[0]
        day_converted = datetime.strptime(day,'%Y-%m-%d').date()
        if (day_iterable[1].get_text() == "CLOSED"):
            start_time = "11:59 pm"
            end_time = "11:59 pm"
        else: 
            start_time = re.sub("^0", "", datetime.strptime(day_iterable[1].get_text().split("-")[0],'%I%p ').time().strftime( '%I:%M %p' ))
            end_time = re.sub("^0", "", datetime.strptime(day_iterable[1].get_text().split("-")[1],' %I%p').time().strftime( '%I:%M %p' ))
        open_close_time = helper.build_time_interval(start_time.lower(),end_time.lower(),day_converted)
        open_close_array.append(open_close_time)

    output_dictionary.update({"name":"RSF"})
    output_dictionary.update({"latitude":"37.8685702"})
    output_dictionary.update({"longitude":"-122.2627233"})
    output_dictionary.update({"phone":"510-642-5072"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"description": "The Recreational Sports Facility (RSF) is the University’s largest, most complete fitness center with over 100,000 square feet of activity space, including an Olympic-sized swimming pool, 3 weight rooms, seven basketball courts, seven racquetball/handball courts, six squash courts, treadmills, elliptical trainers, stairmasters, rowing machines and stationary bikes. "})
    output_dictionary.update({"address":" 2301 Bancroft Way, Berkeley, CA 94720"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary
 
 
def memorial_scrapper():
    open_close_array = []
    output_dictionary = {}


    url_memorial = "https://recsports.berkeley.edu/stadium-fitness-center-hours/"

    page = requests.get(url_memorial)
    soup = BeautifulSoup(page.content,"html.parser")
    content = soup.find(class_="minimal_table")
    content_iterable = content.findAll("tr")
   
    
    for i in content_iterable:
        day_iterable = i.findAll("td")
        day = str(datetime.strptime(str(day_iterable[0].get_text().replace(",","")), '%a %b %d')).replace("1900",str(datetime.now().year)).split(" ")[0]
        day_converted = datetime.strptime(day,'%Y-%m-%d').date()
        if (day_iterable[1].get_text() == "CLOSED"):
            start_time = "11:59 pm"
            end_time = "11:59 pm"
        else: 
            start_time = re.sub("^0", "", datetime.strptime(day_iterable[1].get_text().split("-")[0],'%I%p ').time().strftime( '%I:%M %p' ))
            end_time = re.sub("^0", "", datetime.strptime(day_iterable[1].get_text().split("-")[1],' %I%p').time().strftime( '%I:%M %p' ))
        open_close_time = helper.build_time_interval(start_time.lower(),end_time.lower(),day_converted)
        open_close_array.append(open_close_time)

    output_dictionary.update({"name":"Memorial Stadium Fitness Center"})
    output_dictionary.update({"latitude":"37.8703831"})
    output_dictionary.update({"longitude":"-122.2513493"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"phone":"510-642-7796"})
    output_dictionary.update({"description": "The Rec Sports Stadium Fitness Center at Memorial Stadium is a 5,000 square foot workout space located on the west side of the stadium, between Gates 2 and 5. "})
    output_dictionary.update({"address":" 210 Stadium Rim Way, Berkeley, CA 94704"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary
           

def pool_scrapper():
    url_pool = "https://recsports.berkeley.edu/lap-swim/"

def track_scrapper():
    url_track = "https://recsports.berkeley.edu/tracks/"


if __name__ == "__main__":
    memorial_scrapper()

 