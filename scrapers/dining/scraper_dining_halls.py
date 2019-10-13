import requests
import bs4 as bs
import datetime
import copy
import pandas as pd

source = requests.get("https://caldining.berkeley.edu/menus/late-night-menus")
soup = bs.BeautifulSoup(source.content, features='html.parser')
late_night_items = []

for i in soup.select("ul")[16:]:
    for food_item in i.text.strip().split("\n"):
        late_night_items.append(create_food_item(food_item))


menu_urls = [
    "https://caldining.berkeley.edu/menu_xr.php",
    "https://caldining.berkeley.edu/menu_c3.php",
    "https://caldining.berkeley.edu/menu_ckc.php",
    "https://caldining.berkeley.edu/menu_fh.php"
]


dining_halls = {}

for url in menu_urls:
    source = requests.get(url)
    soup = bs.BeautifulSoup(source.content, features='html.parser')

    breakfast_menu = {}
    lunch_menu = {}
    dinner_menu = {}
    late_night_menu = {}

    for item in soup.select("div.desc_wrap_ck3"):
        date = helper.process_date_string(item.a.text.strip())
        period = item.select("h3")[-1].text.strip()
        food_items = []
        current_station = None

        for station in item.select("p"):
            if "N/A" in station.text:
                continue
            if station.text.isupper():
                current_station = station.text.strip()
                continue

            try:
                for food_item_text in station.text.strip().split("\n"):
                    food_item = create_food_item(food_item_text)
                    food_item["station"] = station.current_station

                    for image in station.find_all("img"):
                        food_item["food_types"].append(image.get("title"))

                    food_items.append(food_item)
            except:
                continue
        
        if period == "Breakfast":
            breakfast_menu[date] = food_items
        elif period == "Lunch" or period == "Brunch":
            lunch_menu[date] = food_items
        elif period == "Dinner":
            dinner_menu[date] = food_items

        late_night_menu[date] = late_night_items

    source = requests.get(details_url)
    soup = bs.BeautifulSoup(source.content, features='html.parser')
    data = str(soup.find_all("div", class_="p_body")).split("<p>")
    picture = image_url
    
    for key in dinner_menu.keys():
        if key not in dh_hours[dining_hall_name]:
            # print("wtf ", key, dh_hours[dining_hall_name])
            continue
        
        if key not in dining_halls.keys():
            dining_halls[key] = {}
            
        
        dining_hall = {}
        dining_hall["name"] = dining_hall_name
        dining_hall["address"] = str(lat_long_df[lat_long_df["location"] == dining_hall_name]["address"].values[0])
        dining_hall["latitude"] = float(lat_long_df[lat_long_df["location"] == dining_hall_name]["latitude"])
        dining_hall["longitude"] = float(lat_long_df[lat_long_df["location"] == dining_hall_name]["longitude"])
        dining_hall["phone"] = None
        dining_hall["picture"] = picture
        dining_hall["description"] = description
        dining_hall["picture"] = image_urls

        if key in breakfast_menu.keys():
            dining_hall["breakfast_menu"] = breakfast_menu[key]
        
        if key in lunch_menu.keys():
            dining_hall["lunch_menu"] = lunch_menu[key]
        
        if key in dinner_menu.keys():
            dining_hall["dinner_menu"] = dinner_menu[key]
        
        if key in late_night_menu.keys():
            dining_hall["late_night_menu"] = late_night_menu[key]
            
        dining_hall["open_close_array"] = dh_hours[dining_hall_name][key]

        dining_halls[key][dining_hall_name] = dining_hall

print(dining_halls)