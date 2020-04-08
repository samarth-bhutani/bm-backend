import requests
import bs4 as bs
import pandas as pd
import os.path
import datetime
import helper

def scrape_menus(cafes, cafe_names, cafe_menus_df):
    for cafe_name in cafe_names:

        for index, row in cafe_menus_df[cafe_menus_df["Location"] == cafe_name][1:].iterrows():
            if row["Menu Type"].strip() not in cafes[cafe_name]:
                cafes[cafe_name][row["Menu Type"].strip()] = []

            food_item = {}
            food_item["calories"] = None
            food_item["cost"] = row["Cost"]
            food_item["food_types"] = []
            food_item["name"] = row["Menu Item"]
            food_item["station"] = ""

            cafes[cafe_name][row["Menu Type"].strip()].append(food_item)

'''
The function scrape_details takes a dictionary in as a parameter, and details about each dining hall location are stored in it
'''
def scrape_details(cafes, cafe_names):
    path = os.path.dirname(__file__).split('/')[:-2]
    pathS = ""

    for p in path:
        pathS += p + '/'

    data1 = pd.read_csv("csv_data/latitude_longitudes.csv")
    data2 = pd.read_csv("csv_data/images.csv")

    for cafe_name in cafe_names:
        cafe_dict = cafes[cafe_name]

        cafe_dict["name"] = cafe_name
        cafe_dict["latitude"] = list(data1[data1['name'] == cafe_name]['latitude'])[0]
        cafe_dict["longitude"] = list(data1[data1['name'] == cafe_name]['longitude'])[0]
        cafe_dict["phone"] = None
        cafe_dict["picture"] = list(data2[data2['name'] == cafe_name]['imageurl'])[0]
        cafe_dict["description"] = None
        cafe_dict["address"] = list(data1[data1['name'] == cafe_name]['address'])[0]
        cafe_dict["open_close_array"] = []

def scrape_others():
    '''Objective: Scrape the data on convenience stores and campus restaurants.
       Format: Has 2 dictionaries with arrays appended in the format (Open, Close, DatetimeObject)
       How-to: Find all tables, goes through rows. Goes through all the tr, finds the restaurant, matches it with the key in the corresponding dictionary and appends it
       with the opening closing time.
       a datetime object using helper functions"
       Contributed by Varun A'''
    conv_stores = {"Bear Market (Café 3)":[], "CKCub\n\t\t\t(Clark Kerr)":[],"Cub Market (Foothill)":[], "The Den, featuring Peet's Coffee & Tea (Crossroads)":[]}
    campus_rests = {"The Golden Bear Café":[], "Brown's":[], "Terrace Café":[], "Common Grounds":[],"The Pro Shop":[]}
    months = {1:"jan", 2:"feb", 3:"mar", 4:"apr", 5:"may", 6:"jun", 7:"jul", 8:"aug",9:"nov",10:"oct", 11:"nov", 12:"dec"}
    day = str(helper.get_last_sunday().day)
    monthnum = helper.get_last_sunday().month
    month = months[monthnum]
    url = "https://caldining.berkeley.edu/locations/hours-operation/week-of-" + month + day
    source = requests.get(url)
    soup = bs.BeautifulSoup(source.content, features='html.parser')
    tables = soup.find_all('table', {'class':'spacefortablecells'})
    for i in range(4, 6):
        tab = tables[i]
        table_body = tab.find('tbody')
        rows = table_body.find_all('tr')
        rows = rows[1:]
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 0:
                continue
            key = cols[0]

            for j in range(1, len(cols)):
                if (i == 4):
                    if cols[j] == "Closed":
                        a, b = 0, 0
                    else:
                        times = cols[j].split(';')
                        
                        if len(times) == 1:

                            times2 = times[0].split('–')
                            times2[1] = times2[1][4:]
                            times3 = str(times2[0].replace(" ", ""))
                            times4 = str(times2[1].replace(" ", ""))
                            times5 = times3.replace(".", "")
                            times6 = times4.replace(".", "")
                            a, b = times5, times6

                        else:
                            times11 = times[0].split('–')
                            times12 = times[1].split('–')

                            

                            times13a = str(times11[0].replace(" ", ""))
                            times13b = str(times11[1].replace(" ", ""))

                            times14a = str(times12[0].replace(" ", ""))
                            times14b = str(times12[1].replace(" ", ""))



                            times15a = times13a.replace(".", "")
                            times15b = times13b.replace(".", "")

                            times16a = times14a.replace(".", "")
                            times16b = times14b.replace(".", "")


                            
                            #print(c, d)
                            c,d,a,b = helper.standarize_timestring(times15a),helper.standarize_timestring(times15b),helper.standarize_timestring(times16a),helper.standarize_timestring(times16b)
                            #print(c,d,a,b)

                            bam = helper.get_last_sunday()
                            x = bam + datetime.timedelta(days=j) #get_last_sunday() +
                            current = helper.build_time_interval(c,d,x)
                            conv_stores[key].append(current)
                    bam = helper.get_last_sunday()
                    x = bam + datetime.timedelta(days=j)
                    #print(a, b, x)
                    current = helper.build_time_interval(a,b,x)
                    conv_stores[key].append(current)
                if (i == 5):
                    if cols[j] == "Closed":
                        a, b = '0', '0'
                    else:
                        times = cols[j].split(',')
                        if len(times) == 1:

                            times2 = times[0].split('–')
                            times2[1] = times2[1][4:]
                            times3 = str(times2[0].replace(" ", ""))
                            times4 = str(times2[1].replace(" ", ""))
                            times5 = times3.replace(".", "")
                            times6 = times4.replace(".", "")
                            a, b = times5, times6
                            #a, b = times2[0], times2[1]

                        else:
                            times2 = times[0].split('–')
                            times3 = times[1].split('–')
                            c,d,a,b = standarize_timestring(times3[0]),standarize_timestring(times3[1]),standarize_timestring(times2[0]),standarize_timestring(times2[1])
                            bam = helper.get_last_sunday()
                            x = bam + datetime.timedelta(days=j) #get_last_sunday() +
                            current = helper.build_time_interval(c,d,x)
                            campus_rests[key].append(current)
                    bam = helper.get_last_sunday()
                    x = bam + datetime.timedelta(days=j) #get_last_sunday() +
                    current = helper.build_time_interval(a,b,x)
                    campus_rests[key].append(current)
       
#call this to actually return the dictionary"
def scrape():
    path = os.path.dirname(__file__).split('/')[:-2]
    pathS = ""

    for p in path:
        pathS += p + '/'

    cafe_menus_df = pd.read_csv("csv_data/cafe_menu.csv")
    cafe_names = list(set(cafe_menus_df["Location"]))

    cafes_information = {}
    for cafe_name in cafe_names:
        cafes_information[cafe_name] = {}

    scrape_details(cafes_information, cafe_names)
    scrape_menus(cafes_information, cafe_names, cafe_menus_df)
    scrape_others()

    return cafes_information
