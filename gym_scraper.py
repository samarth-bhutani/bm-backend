import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import helper
import re
from os.path import dirname, abspath
import os, json, pandas as pd, re
import helper

def primary_scrapper(url):
    ## This is the primary scrapper for athletic facilites. It is used
    ## when a only a SINGLE facility is loaded per webpage/table.

    open_close_array = []
    page = requests.get(url)
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
            continue ## If the facility is closed, then we are not adding a time interval into the array.
        else: 
            start_time = re.sub("^0", "", datetime.strptime(day_iterable[1].get_text().split("-")[0],'%I%p ').time().strftime( '%I:%M %p' ))
            end_time = re.sub("^0", "", datetime.strptime(day_iterable[1].get_text().split("-")[1],' %I%p').time().strftime( '%I:%M %p' ))
        open_close_time = helper.build_time_interval(start_time.lower(),end_time.lower(),day_converted)
        open_close_array.append(open_close_time)

    return open_close_array
           
def event_helper(event):
    ## This is a helper function that analyzes text to determine if a facility is open.

    if "Closure" in event:
        return False
    if "No" in event:
        return False
    else:
        return True

def secondary_scrapper(facility,url):
   ## This is the seconary scrapper, used when MULTIPLE facilities are loaded
   ## on a table/per page.

    open_close_array = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")
    content = soup.find(class_="entry-content")
    list_of_days = content.findAll(class_="fancy_header")
    content = soup.findAll(class_="minimal_table")

    for i, d in zip(content, list_of_days):
        date = d.find(class_="slategrey").get_text()
        revised_date = datetime.strptime(date,"%A, %B %d").date()
        revised_date = revised_date.replace(int(datetime.now().year))

        content_iterable = i.findAll("tr")
        for x in content_iterable:
            if (x.findAll("td") == []):
                continue
            day_iterable = x.findAll("td")
            time = day_iterable[0].get_text().split("-")
            start_time = re.sub(r"([0-9:]+(\.[0-9]+)?)",r" \1 ", time[0]).strip()
            end_time = re.sub(r"([0-9:]+(\.[0-9]+)?)",r" \1 ", time[1]).strip()
            open_close_time = helper.build_time_interval(start_time,end_time,revised_date)
            location = day_iterable[1].get_text()
            event = day_iterable[2].get_text()
            if (location == facility):
                #open_close_array.append(open_close_time)
                if (event_helper(event) == True):
                    open_close_array.append(open_close_time)

    return open_close_array

def memorial_scrapper():
    open_close_array = []
    output_dictionary = {}
    open_close_array = primary_scrapper("https://recsports.berkeley.edu/stadium-fitness-center-hours/")
    output_dictionary.update({"name":"Memorial Stadium Fitness Center"})
    output_dictionary.update({"latitude":37.8703831})
    output_dictionary.update({"longitude":-122.2513493})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"phone":"510-642-7796"})
    output_dictionary.update({"description": "The Rec Sports Stadium Fitness Center at Memorial Stadium is a 5,000 square foot workout space located on the west side of the stadium, between Gates 2 and 5. "})
    output_dictionary.update({"address":" 210 Stadium Rim Way, Berkeley, CA 94704"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary

def rsf_scrapper():

    open_close_array = []
    output_dictionary = {}
    open_close_array = primary_scrapper("https://recsports.berkeley.edu/stadium-fitness-center-hours/")
    output_dictionary.update({"name":"RSF"})
    output_dictionary.update({"latitude":37.8685702})
    output_dictionary.update({"longitude":-122.2627233})
    output_dictionary.update({"phone":"510-642-5072"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"description": "The Recreational Sports Facility (RSF) is the University’s largest, most complete fitness center with over 100,000 square feet of activity space, including an Olympic-sized swimming pool, 3 weight rooms, seven basketball courts, seven racquetball/handball courts, six squash courts, treadmills, elliptical trainers, stairmasters, rowing machines and stationary bikes. "})
    output_dictionary.update({"address":" 2301 Bancroft Way, Berkeley, CA 94720"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary

def hearst_pool_scrapper():
    url_pool = "https://recsports.berkeley.edu/lap-swim/"
    output_dictionary = {}
    location = 'Hearst North Pool'
    open_close_array = secondary_scrapper(location,url_pool)
    output_dictionary.update({"name":"Hearst North Pool"})
    output_dictionary.update({"latitude":37.8697646})
    output_dictionary.update({"longitude":-122.256941})
    output_dictionary.update({"phone":"(510)-642-3894"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"description": "Hearst Pool offers regular lap swim hours and includes amenities such as locker rooms, hot showers, day locks, swim suit spinners, and towel service."})
    output_dictionary.update({"address":" Bancroft Way & Bowditch St, Berkeley, CA 94704"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary
    
def grbc_pool_scrapper():
    url_pool = "https://recsports.berkeley.edu/lap-swim/"
    output_dictionary = {}
    location = 'GBRC'
    open_close_array = secondary_scrapper(location,url_pool)
    output_dictionary.update({"name":"GRBC Pool"})
    output_dictionary.update({"latitude":37.86865280})
    output_dictionary.update({"longitude":-122.247158})
    output_dictionary.update({"phone":"(510)-643-9021"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"description": "The pool includes six lanes that are 25 yards in length with water temperature kept at 80-81 degrees F. The shallow end is three and a half feet deep and the deep end is ten feet deep. Open recreation lap swim only. Amenities include locker rooms, hot showers, lockers (bring your own lock), swimsuit spinners, and kickboards. No towel service is available."})
    output_dictionary.update({"address":"25 Sports Ln, Berkeley, CA 94720"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary

def spieker_pool_scrapper():
    url_pool = "https://recsports.berkeley.edu/lap-swim/"
    output_dictionary = {}
    location = 'Spieker Pool'
    open_close_array = secondary_scrapper(location,url_pool)
    output_dictionary.update({"name":"Spieker Pool"})
    output_dictionary.update({"latitude":37.869229})
    output_dictionary.update({"longitude":-122.262111})
    output_dictionary.update({"phone":"(510)-643-8038"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"description": "Spieker is used for lap swimming, team practice, swim meets and water polo matches. Amenities include locker rooms, hot showers, day locks, swimsuit spinners, kickboards, a pool lift for those needing assistance getting into the pool, wheelchair access to locker rooms, and towel service."})
    output_dictionary.update({"address":" 2301 Bancroft Way, Berkeley, CA 94704"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary

def track_scrapper():
    url_track = "https://recsports.berkeley.edu/tracks/"
    output_dictionary = {}
    location = 'Edwards Track'
    open_close_array = secondary_scrapper(location,url_track)
    output_dictionary.update({"name":"Edwards Track"})
    output_dictionary.update({"latitude":37.869495})
    output_dictionary.update({"longitude":-122.264633})
    output_dictionary.update({"phone":"(510)-643-8038"})
    output_dictionary.update({"picture":None})
    output_dictionary.update({"description": "Edwards Track is an eight-lane running track that is open for recreational use by Rec Sports members when not being used by the Track & Field team."})
    output_dictionary.update({"address":" 2223 Fulton St, Berkeley, CA 94704"})
    output_dictionary.update({"open_close_array":open_close_array})
    return output_dictionary


def virtual_5k_scraper():
    output_dictionary = {}
    output_dictionary.update({"name":"Virtual 5K Run and Walk"})
    output_dictionary.update({"latitude":37.8685702})
    output_dictionary.update({"longitude":-122.2627233})
    output_dictionary.update({"description": "Get moving, have fun, and connect with friends when you join our campus community for virtual 5K events every Saturday. To participate just download the free Strava app and join the Berkeley Rec Sports 5K Club. Complete your 5K at any time during each designated event day. Your choice: Go outside to run or walk (six feet apart!) or stay inside on a treadmill. If you use a treadmill for your 5K you will need to manually enter your participation information onto the app. Check the app messaging posts for event updates and fun fitness tips."})
    output_dictionary.update({"link":"https://www.strava.com/clubs/berkeley-rec-sports-virtual-5k-club-633847"})
    output_dictionary.update({"app":"https://www.strava.com/mobile"})
    
    return output_dictionary

def adventures_scraper():
    
    #name	 description	 link	 address	phone	picture

    parent_working_directory = os.path.dirname((abspath(__file__)))

    data =  pd.read_csv(parent_working_directory + "/csv_data/outdoor_excursions.csv", engine='python')
    data = data.fillna("Not Available")

    #Extract column names
    fields = data.columns.values

    #Loop through each row in csv
    adventures = []
    for row in data.iterrows():
        adventure = {}

        #Loop through each column for each row.
        for i in range(len(data.T)):
            adventure[fields[i]] = row[1][i]

        adventures.append(adventure)
    
    return adventures



def scrape():
    array_of_results = []

    # NOTE: Due to COVID, suspending gyms
    array_of_results.append(memorial_scrapper())
    array_of_results.append(rsf_scrapper())
    array_of_results.append(hearst_pool_scrapper())
    array_of_results.append(grbc_pool_scrapper())
    array_of_results.append(spieker_pool_scrapper())
    array_of_results.append(track_scrapper())
    array_of_results.append(virtual_5k_scraper())
    for adventure in adventures_scraper():
        array_of_results.append(adventure)

    return array_of_results
