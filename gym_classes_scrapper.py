import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import helper
import unidecode


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
        day = class_time.find(class_="hc_starttime").get("data-datetime").split("T")[0]

        ##Class date
        day = datetime.strptime(day,'"%Y-%m-%d').date()

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
        try:
            start_time =  datetime.strptime(class_time_frame[0]," %I:%M %p ").time()
        except:
            pass
        try:
            start_time = datetime.strptime(class_time_frame[0],"%I:%M %p ").time()
        except:
            pass

        #Class end time
        end_time = datetime.strptime(class_time_frame[1],"  %I:%M %p").time()
        
        
        class_dictionary["trainer"] = class_trainer
        class_dictionary['class'] = class_name
        class_dictionary['location'] = class_location
        class_dictionary['class type'] = class_type
        class_dictionary['date'] = day
        class_dictionary["start_time"] = start_time
        class_dictionary["end_time"] = end_time
        class_dictionary['description'] = class_description
        output.append(class_dictionary)



    ## Data Processing: Getting Data into requested schema.
    for i in output:
        date_key = i.get("date").strftime("%Y %m %d")
        if (date_dictionary.get(date_key) == None):
            date_dictionary[date_key] = [i]
        else:
            date_dictionary[date_key].append(i)
    return date_dictionary


    ### Commented Out: Original data processing scheme.
    # Data Processing: Getting Data into requested schema.
    # for i in output:
    #     date_key = i.get("date")
    #     if (date_dictionary.get(date_key) == None):
    #         date_dictionary[date_key] = [i]
    #     else:
    #         date_dictionary[date_key].append(i)
    # list_of_keys = date_dictionary.keys()
    # # Final output dictionary
    # output_dict = {}
    # for k in list_of_keys:
    #     array_of_classes = date_dictionary.get(k)
    #     date_dict = {}
    #     for c in array_of_classes:
    #         class_name_2 = c.get("class")
    #         date_dict[class_name_2] = c
    #     output_dict[k] = date_dict





if __name__ == "__main__":
    scrapper()

 