import requests
import bs4 as bs
import os
import pandas as pd
import datetime
import helper
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import re

month_num_to_month_long = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August",9:"September",10:"October", 11:"November", 12:"December"}
month_long_to_month_num = {value : key for (key, value) in month_num_to_month_long.items()}


def convert_stringdate_to_datetime(date):
    date = date.split(" ")
    year = helper.get_last_sunday().year

    month_num = month_long_to_month_num[date[0]]

    return datetime.datetime(year, month_num, int(date[1]))


def scrape_menus(dining_halls, menu_urls, dining_hall_names):
    def get_late_night_menu(menu):
        meal_type = "Late Night"
        menu[meal_type] = []

        items = [
            "BREAKFAST, Pancakes(2)",
            "BREAKFAST, Chocolate Chip Pancakes(2)",
            "BREAKFAST, Breakfast Burrito",
            "BREAKFAST, Cinnamon Fritters",

            "FRIED, Chicken Strips(4)",
            "FRIED, Buffalo Wings(6)",
            "FRIED, Buffalo Wings(12)",
            "FRIED, Regular Fries",
            "FRIED, Tater Tots",

            "GRILLED AND PLATED, Hamburger",
            "GRILLED AND PLATED, Cheeseburger",
            "GRILLED AND PLATED, Double Burger",
            "GRILLED AND PLATED, Double Cheeseburger",
            "GRILLED AND PLATED, Hot Dog",
            "GRILLED AND PLATED, Grilled Cheese(Vegetarian)",
            "GRILLED AND PLATED, Malibu Burger(Vegetarian)",
            "GRILLED AND PLATED, Mac & Cheese(Vegetarian)",
            "GRILLED AND PLATED, Cheese Quesadilla",
            "GRILLED AND PLATED, Vegan Dog with Vegan Chili and Vegan Cheese",
            "GRILLED AND PLATED, Vegan Dog",
            "GRILLED AND PLATED, Bowl of Chili",
            "GRILLED AND PLATED, Fruit Cup",


            "CONDIMENTS, Sour Cream",
            "CONDIMENTS, Shredded Cheddar",
            "CONDIMENTS, Guacamole",


            "DESSERTS, Cookie à-la-carte",
            "DESSERTS, Milk and Cookies (2)",


            "BEVERAGES, Soda (20 oz)",
            "BEVERAGES, Milk (Half pint)",
        ]

        for item in items:
            x,y = item.split(", ")
            food_item = {}
            food_item["calories"] = 0
            food_item["cost"] = 0
            food_item["food_types"] = []
            food_item["name"] = y
            food_item["station"] = x

            menu[meal_type].append(food_item)

    for url, dining_hall_name in zip(menu_urls, dining_hall_names):
        # NOTE: Hardcoded since Foothill is closed for Fall 2020
        if dining_hall_name == "Foothill":
            continue

        source = requests.get(url)
        s0 = bs.BeautifulSoup(source.content, features='html.parser')

        for item in s0.select("div.menu_wrap_overall"):
            date = None
            menu = {}

            for meal in item.select("div.desc_wrap_ck3"):
                date = meal.select("h3.location_name")[0].text.split(", ")[1]
                meal_type = meal.select("h3.location_period")[0].text.strip()
                menu[meal_type] = []

                food_items = [i.text for i in meal.select("p")]
                food_restrictions = [[j.get("title") for j in i.select("img.food_icon")] for i in meal.select("p")]

                index = 0
                current_station = None

                for i in food_items:
                    if i.isupper():
                        current_station = i
                    else:
                        food_item = {}
                        food_item["calories"] = None
                        food_item["cost"] = None
                        food_item["food_types"] = food_restrictions[index]
                        food_item["name"] = i.strip()
                        food_item["station"] = current_station.strip()

                        menu[meal_type].append(food_item)

                        index += 1

            # get_late_night_menu(menu)

            dining_halls[dining_hall_name]["menu"][convert_stringdate_to_datetime(date)] = menu


'''
The function scrape_details takes a dictionary in as a parameter, and details about each dining hall location are stored in it
'''
def scrape_details(dining_halls, dining_hall_names):
    data1 = pd.read_csv("csv_data/latitude_longitudes.csv")
    data2 = pd.read_csv("csv_data/images.csv")

    

    index = 0
    for dining_hall_name in dining_hall_names:

        dining_hall_dict = dining_halls[dining_hall_name]

        dining_hall_dict["name"] = dining_hall_name
        dining_hall_dict["latitude"] = list(data1[data1['name'] == dining_hall_name]['latitude'])[0]
        dining_hall_dict["longitude"] = list(data1[data1['name'] == dining_hall_name]['longitude'])[0]
        dining_hall_dict["phone"] = None
        dining_hall_dict["menu"] = None
        dining_hall_dict["picture"] = list(data2[data2['name'] == dining_hall_name]['imageurl'])[0]
        dining_hall_dict["description"] = None
        dining_hall_dict["address"] = list(data1[data1['name'] == dining_hall_name]['address'])[0]
        dining_hall_dict["open_close_array"] = scrape_times(index)

        dining_hall_dict["menu"] = {}

        index += 1

def scrape_times(index):
    '''Objective: Scrape the data on convenience stores and campus restaurants.
       Format: Has 2 dictionaries with arrays appended in the format (Open, Close, Breakfast/Lunch/Dinner, DatetimeObject)
       How-to: Find all tables, goes through rows. Goes through all the tr, finds whether it's Breakfast/Lunch/Dinner and appends it with the opening closing time, adding
       a datetime object using helper functions"
       Contributed by Varun A'''
    day = str(helper.get_last_sunday().day)
    monthnum = helper.get_last_sunday().month
    month = month_num_to_month_long[monthnum]
    url = "https://caldining.berkeley.edu/locations/hours-of-operation/week-of-{0}-{1}/".format(month, day)

    driver = webdriver.Chrome(executable_path = './chromedriver')
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    results = driver.page_source

    driver.quit()

    soup = bs.BeautifulSoup(results, features='html.parser')
    #return as format [(Open, close, date, Breakfast/lunch/dinner), (Open, close, date, Breakfast/lunch/dinner)]
    data = [] #This is where we'll store data
    tables = soup.find_all('table')

    tab = tables[index] #Selects table based on index
    table_body = tab.find('tbody')
    rows = table_body.find_all('tr')

    for row, meal in zip(rows, ["Breakfast", "Lunch", "Dinner"]):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        
        for j in range(0, len(cols)):
            if cols[j] == "Closed":
                a, b = '0', '0'
                bam = helper.get_last_sunday()
                x = bam + datetime.timedelta(days=j)
                current_time = helper.build_time_interval(a,b,x)
                current_time["notes"] = meal

                data.append(current_time)
            else:
                times = cols[j].split(',')
                times = [t.replace(".", "") for t in times]
                times = [t.replace(" ", "") for t in times]
                times = [t.replace(" ", "") for t in times]
                times = [t.split("–") for t in times]


                for time in times:
                    am_pm_arr = ["".join(re.findall("[a-zA-Z]+", t))[:2].strip().lower() for t in time]
                    time = ["".join(re.findall("[0-9:]+", t)).strip().lower() for t in time]


                    if len(am_pm_arr[0]) != 2:
                        time[0] = time[0] + am_pm_arr[-1]
                        time[1] = time[1] + am_pm_arr[-1]
                    else:
                        time[0] = time[0] + am_pm_arr[0]
                        time[1] = time[1] + am_pm_arr[1]
                            
                    a, b = helper.standarize_timestring(time[0]), helper.standarize_timestring(time[1])
                    
                    bam = helper.get_last_sunday()
                    x = bam + datetime.timedelta(days=j)
                    current_time = helper.build_time_interval(a,b,x)
                    current_time["notes"] = meal

                    data.append(current_time)

    return data
       

def scrape():
    dining_halls = {}
    dining_halls["Crossroads"] = {}
    dining_halls["Cafe 3"] = {}
    dining_halls["Clark Kerr"] = {}
    dining_halls["Foothill"] = {}


    menu_urls = [
        "https://caldining.berkeley.edu/dining-menu/cafe-3/",
        "https://caldining.berkeley.edu/dining-menu/crossroads/",
        "https://caldining.berkeley.edu/dining-menu/clark-kerr/",
        "https://caldining.berkeley.edu/dining-menu/foothill/"
    ]

    dining_hall_names = [
        "Crossroads",
        "Cafe 3",
        "Clark Kerr",
        "Foothill"
    ]


    dining_halls_information = {
        "Cafe 3":{},
        "Clark Kerr":{},
        "Crossroads":{},
        "Foothill":{}
    }

    scrape_details(dining_halls_information, dining_hall_names)
    scrape_menus(dining_halls_information, menu_urls, dining_hall_names)

    return dining_halls_information