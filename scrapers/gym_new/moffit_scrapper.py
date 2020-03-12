import requests
from bs4 import BeautifulSoup
import json
import urllib
import helper
import urllib3
import xml.etree.ElementTree as etree
import urlopen

class Date:
    ## Creates date object so correct type is passed into helper functions.
    def __init__(self,date):
        self.date = date
        date_array = self.date.split("-")
        self.day = int(date_array[2])
        self.month = int(date_array[1])
        self.year = int(date_array[0])


def output_to_json(array_of_times):
    ## Outputs scrapped data to JSON file format.
    with open('gym.txt', 'w') as json_file:
        for i in array_of_times:
            json.dump(i,json_file, indent = 4, sort_keys = False)

def scrapper():
    ## Moffit scrapper function, extracts data online.
 
    url = "https://recsports.berkeley.edu/group-ex-schedule/"
    api_call = "https://widgets.mindbodyonline.com/widgets/schedules/8d3262c705.json?mobile=false&version=0.1"
    #page = requests.get(api_call)
    page = urlopen(api_call)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(page, htmlparser)

    #data = json.load(urllib.request.urlopen(url))
    #tree = ET.fromstring(page.content)
    soup = BeautifulSoup(page.content,'html.parser')
    soup.find()


    # Array will hold all the scrapped open/close times.
    output_array = []

    #Array will hold all the data that will need to be exported to JSON format.
    JSON_array = []
 
    # #Scrapped master list of open/close times, stored in array.
    # master_list = data[0]["hours"]
 
    # # Master list of hours, will loop through it.
    # for i in master_list:

    #     #Default start and end values
    #     start_time = i["day"]["start"]
    #     end_time = i["day"]["end"]
    #     date = i["day"]["day"]
    #     date_converted = Date(date)
      
        
    #     #Edge Case 1: When start time is none, '9am - '
    #     if (start_time == None):
    #         start_time = i["day"]["note"]

    #     ## Edge Case 2: When end time is none, 24 hours
    #     if (end_time == None and start_time != i["day"]["note"]):
    #         end_time = i["day"]["note"]

    #     ## Edge Case 3: Start time is 24 hous
    #     if (start_time == "24 hours" and end_time == None):
    #         start_time = "12:00 am"
    #         end_time = "11:59 pm"

    #     if (end_time == None):
    #         end_time = "11:59 pm"

    #     ## Edge Case 4A Library is closed, but opens next day.
    #     if (start_time == None and end_time == '11:59 pm'):
    #         start_time = "11:59 pm"

    #     ## Edge Case 4B Library is closed, closed on next day.    
    #     if (start_time == None and end_time == None):
    #         start_time = "11:59 pm"
    #         end_time = "11:59 pm"

    #     ## Edge Case 5: Fridays, closes at X time.
    #     if ("Close" in start_time):
    #         time_parsing = start_time.split("at ")
    #         start_time = "12:00 am"
    #         end_time = time_parsing[1]

      
        # output = helper.build_time_interval(start_time,end_time,date_converted)
        # output_array.append(output)



    JSON_array.append({"name":"Moffitt Library"})
    JSON_array.append({"latitude":"37.87277"})
    JSON_array.append({"longitude":"-122.260244"})
    JSON_array.append({"phone":"510-642-5072"})
    JSON_array.append({"picture":None})
    JSON_array.append({"phone":"510-642-5072"})
    JSON_array.append({"description":None})
    JSON_array.append({"address":"350 Moffitt Library, Berkeley, CA 94720"})
    JSON_array.append({"open_close_array":output_array})
    

    #Calls output_to_json file
    #output_to_json(JSON_array)



if __name__ == "__main__":
    scrapper()

 