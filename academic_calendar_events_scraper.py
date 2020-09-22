import re, requests
from datetime import datetime, timedelta
import unidecode as u
from bs4 import BeautifulSoup
from multiprocessing import Pool
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import helper
from os.path import dirname, abspath
import os
import helper

def scrape():
    result = {}
    
    parent_working_directory = os.path.dirname((abspath(__file__)))
    data =  pd.read_csv(parent_working_directory + "/csv_data/ace20-21.csv", engine='python')
    data = data.fillna("Not Available")

    #Extract column names
    fields = data.columns.values

    #Loop through each row in csv
    count = 1
    for row in data.iterrows():
        event = {}

        #Loop through each column for each row.
        for i in range(len(data.T)):
            event[fields[i]] = row[1][i].strip()

        event["event_date"] = "".join(event["event_date"].split(",")[1:]).strip()
        event["event_date"] =  datetime.strptime(event["event_date"], '%B %d %Y')
        event["event_date"] = helper.convert_to_posix(None, event["event_date"].day, event["event_date"].month, event["event_date"].year)


        result["Event {}".format(count)] = event
        count += 1

    return result

