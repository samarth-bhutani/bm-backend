import requests
import bs4 as bs
import datetime
from helper import *

dining_halls = {}
dining_halls["Crossroads"] = {}
dining_halls["Cafe 3"] = {}
dining_halls["Clark Kerr"] = {}
dining_halls["Foothill"] = {}


menu_urls = [
    "https://caldining.berkeley.edu/menu_xr.php",
    "https://caldining.berkeley.edu/menu_c3.php",
    "https://caldining.berkeley.edu/menu_ckc.php",
    "https://caldining.berkeley.edu/menu_fh.php"
]

dining_hall_names = [
    "Crossroads",
    "Cafe 3",
    "Clark Kerr",
    "Foothill"
]

'''
THe function scrape_menus takes a dictionary in as a parameter, and the menu is stored into the dictionary that is passed.
'''
def scrape_menus(dining_halls):
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
                        food_item["name"] = i
                        food_item["station"] = current_station

                        menu[meal_type].append(food_item)

                        index += 1

            get_late_night_menu(menu)


            dining_halls[dining_hall_name][date] = menu


'''
The function scrape_details takes a dictionary in as a parameter, and details about each dining hall location are stored in it
'''
def scrape_details(dining_halls):
    index = 0
    for dining_hall_name in dining_hall_names:

        dining_hall_dict = dining_halls[dining_hall_name]

        dining_hall_dict["name"] = dining_hall_name
        dining_hall_dict["latitude"] = None
        dining_hall_dict["longitude"] = None
        dining_hall_dict["phone"] = None
        dining_hall_dict["picture"] = None
        dining_hall_dict["description"] = None
        dining_hall_dict["address"] = None
        dining_hall_dict["open_close_array"] = scrape_times(index)
        index+=1

def scrape_times(index):
    '''Objective: Scrape the data on convenience stores and campus restaurants.
       Format: Has 2 dictionaries with arrays appended in the format (Open, Close, Breakfast/Lunch/Dinner, DatetimeObject)
       How-to: Find all tables, goes through rows. Goes through all the tr, finds whether it's Breakfast/Lunch/Dinner and appends it with the opening closing time, adding
       a datetime object using helper functions"
       Contributed by Varun A'''
    months = {1:"jan", 2:"feb", 3:"march", 4:"april", 5:"may", 6:"june", 7:"july", 8:"august",9:"nov",10:"oct", 11:"nov", 12:"dec"}
    day = str(get_last_sunday().day)
    monthnum = get_last_sunday().month
    month = months[monthnum]
    url = "https://caldining.berkeley.edu/locations/hours-operation/week-of-" + month + day
    
    source = requests.get(url)
    soup = bs.BeautifulSoup(source.content, features='html.parser')
    #return as format [(Open, close, date, Breakfast/lunch/dinner), (Open, close, date, Breakfast/lunch/dinner)]
    data = [] #This is where we'll store data
    tables = soup.find_all('table', {'class':'spacefortablecells'})
    tab = tables[index] #Selects table based on index
    table_body = tab.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        for j in range(0, len(cols)):
            if j == 0:
                meal = cols[j]
                continue
            if cols[j] == "Closed":
                a, b = 0, 0
            else:
                times = cols[j].split(',')
                times2 = times[0].split('-')
                a, b = standarize_timestring(times2[0]), standarize_timestring(times2[1])
                bam = get_last_sunday()
                x = bam + datetime.timedelta(days=j)
                current_time = build_time_interval(a,b,x)
                #Maybe call build_time internval here on (a,b,x)
                current = (current_time, meal)
                data.append(current)
    print(data)


dining_halls_information = {
    "Cafe 3":{},
    "Clark Kerr":{},
    "Crossroads":{},
    "Foothill":{}
}

#scrape_menus(dining_halls_information)
scrape_details(dining_halls_information)
#scrape_others()
#print(dining_halls_information)