import requests
from bs4 import BeautifulSoup as bs
import time 
import json
import datetime 
import helper

libraries = {}
library_names = ["Anthropology Library", "Art History/Classics Library", "BAMPFA Film Library & Study Center", "Bancroft Library/University Archives", "Berkeley Law Library", "Bioscience, Natural Resources & Public Health Library", "Business Library", "Career Counseling Library",
"CED Visual Resources Center", "Chemistry and Chemical Engineering Library", "Doe Library", "Earth Sciences & Map Library", "East Asian Library", "Engineering Library", "Environmental Design Library", "Ethnic Studies Library", "Graduate Theological Union Library", "Institute of Governmental Studies Library", "Institute of Transportation Studies Library", "Main (Gardner) Stacks", "Mathematics Statistics Library", "Moffitt Library", "Morrison Library", "Music Library", "Newspapers & Microforms Library", "Optometry and Health Sciences Library", "Physics-Astronomy Library", "Robbins Collection Library", "Social Research Library", "South/Southeast Asia Library"]

def initialize_libraries_dict(libraries, library_names):
    for i in range(len(library_names)):
        library = library_names[i]
        libraries[library] = {}
        libraries[library]["name"] = library_names[i]
        libraries[library]["latitude"] = None
        libraries[library]["longitude"] = None
        libraries[library]["phone"] = None
        libraries[library]["picture"] = None
        libraries[library]["description"] = None
        libraries[library]["address"] = None
        libraries[library]["open_close_array"] = []

def set_library_ids(libraries):
    '''
    Sets library id in the libraries dictionary. 
    libraries[id] = int 
    Hardcoded because the JSON api arbitrarily assigns library ids. 
    '''
    libraries["Anthropology Library"]["id"] = 194
    libraries["Art History/Classics Library"]["id"] = 183
    libraries["BAMPFA Film Library & Study Center"]["id"] = 251
    libraries["Bancroft Library/University Archives"]["id"] = 196
    libraries["Berkeley Law Library"]["id"] = 242
    libraries["Bioscience, Natural Resources & Public Health Library"]["id"] = 198
    libraries["Business Library"]["id"] = 200
    libraries["Career Counseling Library"]["id"] = 259
    libraries["CED Visual Resources Center"]["id"] = 228
    libraries["Chemistry and Chemical Engineering Library"]["id"] = 202
    libraries["Doe Library"]["id"] = 173
    libraries["Earth Sciences & Map Library"]["id"] = 204
    libraries["East Asian Library"]["id"] = 206 
    libraries["Engineering Library"]["id"] = 210
    libraries["Environmental Design Library"]["id"] = 212
    libraries["Ethnic Studies Library"]["id"] = 232
    libraries["Graduate Theological Union Library"]["id"] = 249
    libraries["Institute of Governmental Studies Library"]["id"] = 236
    libraries["Institute of Transportation Studies Library"]["id"] = 240
    libraries["Main (Gardner) Stacks"]["id"] = 174 
    libraries["Mathematics Statistics Library"]["id"] = 214
    libraries["Moffitt Library"]["id"] = 179
    libraries["Morrison Library"]["id"] = 200
    libraries["Music Library"]["id"] = 216
    libraries["Newspapers & Microforms Library"]["id"] = 191
    libraries["Optometry and Health Sciences Library"]["id"] = 218
    libraries["Physics-Astronomy Library"]["id"] = 220
    libraries["Robbins Collection Library"]["id"] = 261
    libraries["Social Research Library"]["id"] = 224
    libraries["South/Southeast Asia Library"]["id"] = 192

def parse_hours(day):
    '''
    Takes in a day dictionary and returns list of DateTime object representations of the hours of each day. 
    '''
    datetime_object = datetime.datetime.strptime(day["day"], '%Y-%m-%d')
    date = datetime_object.date()
    hours_list = []
    is_closed = day["closed"] 
    if not is_closed: 
        if day["start"] == None:
            day["start"] = "00:00"
        if day["end"] == None:
            day["end"] = "23:59"
        
        if day["start2"] != None and day["end2"] == None:
            day["end2"] = "23:59"

    if is_closed:
        day["start"] = "00:00"
        day["start2"] = None
        day["end"] = "00:00"
        day["end2"] = None

    if day["start"] != None and day["start"] != '' and day["end"] != None and day["end"] != '':
        hours_list.append((
            helper.standarize_timestring(day["start"]),
            helper.standarize_timestring(day["end"]),
            date))

    if day["start2"] != None and day["start2"] != '' and day["end2"] != None and day["start2"] != '':
        hours_list.append((
            helper.standarize_timestring(day["start2"]),
            helper.standarize_timestring(day["end2"]),
            date))

    return hours_list
    
def get_library_url(library_id): 
    '''
    Returns the JSON api url of the given library, identified by library_id, for the current week.
    '''
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

def scrape_library_hours(libraries, library_names): 
    '''
    Scrapes library hours from library urls and stores it into the libraries dictionary.
    '''
    for library_name in library_names:
        library_dict = libraries[library_name]
        library_id = library_dict["id"]
        url = get_library_url(206)
        try:
            response = requests.get(url)
            response_page_json = response.json()
            response_json = response_page_json[0]
            hours_dict = response_json["hours"]
            # print(len(hours_dict))
            for days in hours_dict:
                # print(days)

                day_hours = parse_hours(days["day"])
                for item in day_hours:
                    # print(item)
                    library_dict["open_close_array"].append(helper.build_time_interval(*item))
        except Exception as e:
            '''
            Edge cases: Library doesn't have start, end time. Has "closed" or some text? 
            
            Library JSON API url has multiple dictionaries >>> json.loads() doesn't like that. 
            '''
            print(str(e))
            print("Exception has occurred for library with id: {0}.".format(library_id))
"""
    1. Initilize libraries dictionary
    2. Set the library ids for each library id. Hardcoded values because the ids are unique.
    3. Go through the JSON API for each library page and get data from the JSON. 
    4. Output a JSON file with all the values.
"""
initialize_libraries_dict(libraries, library_names)
set_library_ids(libraries)
scrape_library_hours(libraries, library_names)

with open("libraries.json", "w") as outfile:
    json.dump(libraries, outfile)