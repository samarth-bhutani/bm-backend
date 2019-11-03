from selenium import webdriver
from models import GymClass
import time
import json

import os, sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from helper import *
import datetime

RSF_CLASSES = "https://recsports.berkeley.edu/group-ex-schedule/"

def parse_name_room(title):
    arr = title.split("(")
    name = arr[0]
    if (len(arr) > 1):
        room = arr[1].split(")")[0]
    else:
        room = ""
    return name, room

def parse_hour_string(hours):
    open_close = hours.split(" - ")
    if len(open_close) == 1:
        return "", ""
    else:
        return open_close[0], open_close[1]

def parse(browser):
    for j in range(7):
        class_blocks = browser.find_elements_by_xpath("//main/article/section/p/healcode-widget/div[@class='healcode schedule  mindbody_classic']/table/tbody/tr[@data-hc-day=" + str(j) + "]/td/span")
        class_dict[j] = []
        i = 0
        
        day, week_of_day, week_of_mon = get_last_sunday()

        while i < len(class_blocks):
            new_class = GymClass()
            new_class.name, new_class.room = parse_name_room(class_blocks[i + 3].text)
            new_class.start_time, new_class.end_time = parse_hour_string(class_blocks[i].text)
            new_class.start_time = convert_to_timestamp_seconds(get_24_hr_time(new_class.start_time), day.day, day.month, day.year)
            new_class.end_time = convert_to_timestamp_seconds(get_24_hr_time(new_class.end_time), day.day, day.month, day.year)
            new_class.trainer = class_blocks[i + 5].text
            new_class.type = class_blocks[i + 4].text
            class_dict[j].append(new_class)
            i += 6
            day += datetime.timedelta(days=1)

def output_file():
    if (len(class_dict) == 7):
        with open('gym_classes.json', 'w') as outfile:
            json.dump(class_dict, outfile, default=lambda o: o.__dict__)

class_dict = dict()

browser = webdriver.Chrome(executable_path='/Applications/chromedriver')
# browser = webdriver.Chrome(executable_path='/home/dellxps13/octo/asuc-backend/scrapers/gyms/chromedriver_linux64/chromedriver')

browser.get(RSF_CLASSES)
time.sleep(3)
parse(browser)
browser.quit()
time.sleep(3)
output_file()
