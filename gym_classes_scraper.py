import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import helper
import unidecode


class Date:
    ## Creates date object so correct type is passed into helper functions.
    def __init__(self,date):
        self.date = date
        date_array = self.date.split("-")
        self.day = int(date_array[2])
        self.month = int(date_array[1])
        self.year = int(date_array[0])

def scrapper():
    ## Gym classes scrapper function, extracts data online.
    api_call = "https://widgets.mindbodyonline.com/widgets/schedules/8d3262c705.json?mobile=false&version=0.1"
    page = requests.get(api_call)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(json.loads(page.content)['contents'],'html.parser')
    data = soup.findAll(class_="DropIn")
    

    # Output dictionary = level 0
    output = []
  
    # Date dictonary = level 1
    date_dictionary = {}
 
    for i in data:

    
        # Class dictionary = level 3
        class_dictionary = {}


        class_content = i.find(class_="mbo_class")
        class_time = i.find(class_="hc_time")
        day = class_time.find(class_="hc_starttime").get("data-datetime").split("T")[0].replace('"',"")

        ##Class Type
        class_type = unidecode.unidecode(i.find(class_="visit_type").get_text())
        class_type = class_type.replace("\n","")

        ##Trainer's name 
        class_trainer = unidecode.unidecode(i.find(class_="trainer").get_text())
        class_trainer = class_trainer.replace("\n","")

    
        ##Class name and location
        class_name_and_location = class_content.find(class_="classname").get_text().split("(")
        class_name = class_name_and_location[0].rstrip('\n')
        try:
            class_location = class_name_and_location[1].split(")")[0]
        except:
            pass
       
        ## Second API call to get class content details (descriptions)
        class_description_url = class_content.find("a", {'data-hc-open-modal': 'modal-iframe'}).get("data-url")
        content_detail = requests.get(class_description_url)
        soup_content = BeautifulSoup(content_detail.content,'html.parser')

        ##Class description
        class_description = unidecode.unidecode(soup_content.find(class_="class_description").get_text().rstrip('\n'))
       
        ##Class start time, multiple cases needed due to inconsistent formatting.
        class_time_frame = class_time.get_text()
        class_time_frame = class_time_frame.split("-")
        start_time = class_time_frame[0].lower().strip()
        end_time = class_time_frame[1].lower().strip()

        #Build time interval
        open_close = helper.build_time_interval(start_time,end_time,Date(day))
        
        class_dictionary["trainer"] = class_trainer
        class_dictionary['class'] = class_name
        class_dictionary['location'] = class_location
        class_dictionary['class type'] = class_type
        class_dictionary['date'] = day
        class_dictionary['description'] = class_description
        class_dictionary["open_close_array"] = open_close
        output.append(class_dictionary)



    # Data Processing: Getting Data into requested schema.
    for i in output:
        date_key = i.get("date")
        if (date_dictionary.get(date_key) == None):
            date_dictionary[date_key] = {i.get('class'):i}
        else:
            date_dictionary[date_key].update({i.get('class'):i})
    
    return date_dictionary
