import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import helper
import unidecode
import re
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Date:
    ## Creates date object so correct type is passed into helper functions.
    def __init__(self,date):
        self.date = date
        date_array = self.date.split("-")
        self.day = int(date_array[2])
        self.month = int(date_array[1])
        self.year = int(date_array[0])


def scrape():
    startTime = helper.get_last_sunday().isoformat() + 'T' + "7:0:0" + 'Z' # 'Z' indicates UTC time
    endTime = helper.get_next_monday().isoformat() + 'T' + "7:0:0" + 'Z' # 'Z' indicates UTC time

    class_types = {
        "Barre-Fit":"STRENGTH",
        "Barre-Fit Express":"STRENGTH",
        "Barre-Pilates Fusion":"STRENGTH",
        "BollyX":"DANCE",
        "Cardio & Core":"CARDIO",
        "Cardio & Core Express":"CARDIO",
        "Dance Jam":"DANCE",
        "Early Bird Yoga":"MIND/BODY",
        "Legs & Glutes":"CARDIO",
        "Mat Pilates":"CARDIO",
        "PiYo":"MIND/BODY",
        "Power Yoga":"MIND/BODY",
        "Simple Strong | TBC":"STRENGTH",
        "Upper Body Blast":"HIIT",
        "UrbanKick":"HIIT",
        "Yoga":"MIND/BODY",
        "Yoga & Meditation":"MIND/BODY",
        "Yoga Stretch":"MIND/BODY",
        "Zumba":"DANCE",
    }

    # Output dictionary = level 0
    output = []
  
    # Date dictonary = level 1
    date_dictionary = {}


    with open('keys/bm-calendar-token-pickle.pickle', 'rb') as token:
        creds = pickle.load(token)

    service = build('calendar', 'v3', credentials=creds)

    

    events_result = service.events().list(
        calendarId='berkeley.edu_vhbqrveo1je1ve9mmdsejmuan0@group.calendar.google.com',
        timeMin=startTime,singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        class_dictionary = {}

        bcalDesc = re.sub(re.compile('<.*?>'), ' ', event["description"])

        class_trainer = bcalDesc.split("How to Participate:")[0][len("Instructor: "):]
        zoom_link = event["description"].split('<a href=\"')[1].split('"')[0]
        class_name = event["summary"]
        class_description = bcalDesc.split("Class Description:")[-1]

        date = datetime.datetime.strptime(event["start"]["dateTime"].split("T")[0], '%Y-%m-%d')
        start_time = event["start"]["dateTime"].split("T")[1][:-9]
        end_time = event["end"]["dateTime"].split("T")[1][:-9]
        open_close = helper.build_time_interval(start_time, end_time, date)

        class_dictionary["trainer"] = class_trainer
        class_dictionary['class'] = class_name
        class_dictionary['location'] = "\nSee recsports.berkeley.edu/online"
        class_dictionary['link'] = zoom_link
        class_dictionary['class type'] = class_types[class_name] if class_name in class_types else "ALL-AROUND WORKOUT"
        class_dictionary['date'] = event["start"]["dateTime"].split("T")[0]
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

scrape()