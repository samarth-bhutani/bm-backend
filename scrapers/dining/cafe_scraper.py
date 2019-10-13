import requests
import bs4 as bs
import pandas as pd
import os.path

path = os.path.dirname(__file__).split('/')[:-2]
pathS = ""

for p in path:
    pathS += p + '/'

cafe_menus_df = pd.read_csv(pathS+ "/csv_data/cafe_menu.csv")
cafe_names = list(set(cafe_menus_df["Location"]))

'''
THe function scrape_menus takes a dictionary in as a parameter, and the menu is stored into the dictionary that is passed.
'''
def scrape_menus(cafes):
    for cafe_name in cafe_names:

        for index, row in cafe_menus_df[cafe_menus_df["Location"] == cafe_name][1:].iterrows():
            if row["Menu Type"].strip() not in cafes[cafe_name]:
                cafes[cafe_name][row["Menu Type"].strip()] = []

            food_item = {}
            food_item["calories"] = 0
            food_item["cost"] = row["Cost"]
            food_item["food_types"] = []
            food_item["name"] = row["Menu Item"]
            food_item["station"] = ""

            cafes[cafe_name][row["Menu Type"].strip()].append(food_item)

'''
The function scrape_details takes a dictionary in as a parameter, and details about each dining hall location are stored in it
'''
def scrape_details(cafes):
    for cafe_name in cafe_names:
        cafe_dict = cafes[cafe_name]

        cafe_dict["name"] = cafe_name
        cafe_dict["latitude"] = ""
        cafe_dict["longitude"] = ""
        cafe_dict["phone"] = ""
        cafe_dict["picture"] = ""
        cafe_dict["description"] = ""
        cafe_dict["address"] = ""
        cafe_dict["open_close_array"] = []



cafes_information = {}
for cafe_name in cafe_names:
    cafes_information[cafe_name] = {}

scrape_menus(cafes_information)
scrape_details(cafes_information)

print(cafes_information)
