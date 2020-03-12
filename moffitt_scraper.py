import requests
from bs4 import BeautifulSoup
import json
import urllib
import helper

class Date:
    ## Creates date object so correct type is passed into helper functions.
    def __init__(self,date):
        self.date = date
        date_array = self.date.split("-")
        self.day = int(date_array[2])
        self.month = int(date_array[1])
        self.year = int(date_array[0])


def get_library_url(library_id): 
# '''
# Returns the JSON api url of the given library, identified by library_id, for the current week.
# '''

    curr_week_dates = helper.get_this_week_dates()
    sunday_datetime = curr_week_dates[0]
    saturday_datetime = curr_week_dates[-1]

    url_p1 = "http://www.lib.berkeley.edu/hours/api/libraries/"
    url_p2 = str(library_id)
    url_p3 = "?begin_date="
    begin_date = str(sunday_datetime.year) + "-" + str(sunday_datetime.month) + "-" + str(sunday_datetime.day)
    url_p4 = "&end_date="
    end_date = str(saturday_datetime.year) + "-" + str(saturday_datetime.month) + "-" + str(saturday_datetime.day)
    url = url_p1 + url_p2 + url_p3 + begin_date + url_p4 + end_date
    return url

def output_to_json(array_of_times):
    ## Outputs scrapped data to JSON file format.
    with open('moffit.txt', 'w') as json_file:
        for i in array_of_times:
            json.dump(i,json_file, indent = 4, sort_keys = False)

def json_to_python(JSON_array):
    y = json.load(JSON_array)
    print(y)

def scrapper():
    ## Moffit scrapper function, extracts data online.
 
    url = get_library_url(179)
    data = json.load(urllib.request.urlopen(url))

    # Array will hold all the scrapped open/close times.
    output_array = []

    #Array will hold all the data that will need to be exported to JSON format.
    JSON_array = {}
 
    #Scrapped master list of open/close times, stored in array.
    master_list = data[0]["hours"]
 
    # Master list of hours, will loop through it.
    for i in master_list:

        #Default start and end values
        start_time = i["day"]["start"]
        end_time = i["day"]["end"]
        date = i["day"]["day"]
        date_converted = Date(date)
      
        
        #Edge Case 1: When start time is none, '9am - '
        if (start_time == None):
            start_time = i["day"]["note"]

        ## Edge Case 2: When end time is none, 24 hours
        if (end_time == None and start_time != i["day"]["note"]):
            end_time = i["day"]["note"]

        ## Edge Case 3: Start time is 24 hous
        if (start_time == "24 hours" and end_time == None):
            start_time = "12:00 am"
            end_time = "11:59 pm"

        if (end_time == None):
            end_time = "11:59 pm"

        ## Edge Case 4A Library is closed, but opens next day.
        if (start_time == None and end_time == '11:59 pm'):
            start_time = "11:59 pm"

        ## Edge Case 4B Library is closed, closed on next day.    
        if (start_time == None and end_time == None):
            start_time = "11:59 pm"
            end_time = "11:59 pm"

        ## Edge Case 5: Fridays, closes at X time.
        if ("Close" in start_time):
            time_parsing = start_time.split("at ")
            start_time = "12:00 am"
            end_time = time_parsing[1]

      
        output = helper.build_time_interval(start_time,end_time,date_converted)
        output_array.append(output)



    JSON_array.update({"name":"Moffitt Library"})
    JSON_array.update({"latitude":"37.87277"})
    JSON_array.update({"longitude":"-122.260244"})
    JSON_array.update({"phone":"510-642-5072"})
    JSON_array.update({"picture":None})
    JSON_array.update({"phone":"510-642-5072"})
    JSON_array.update({"description":None})
    JSON_array.update({"address":"350 Moffitt Library, Berkeley, CA 94720"})
    JSON_array.update({"open_close_array":output_array})
    
    print(JSON_array)
    #json_to_python(JSON_array)
    #Calls output_to_json file
    #output_to_json(JSON_array)



if __name__ == "__main__":
    scrapper()

 