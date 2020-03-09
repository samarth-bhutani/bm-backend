# import os, sys
# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '.')))

import firebase_admin, os, sys, shutil, inspect, json, pandas as pd, scrapers.helper, datetime
from firebase_admin import credentials, firestore
# from post_processing import post_processor
# from integration_test import Testing

# integration_test = Testing()

#update credentials
cred = credentials.Certificate("/Users/sudarshan/Github/asuc-backend/firebase/backend-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

"""
    Helper functions
"""
def scrape_dining_hall_information():
    from scrapers.dining import dining_scraper
    dining_hall_scraper = dining_scraper.DiningHallScraper()
    
    dining_halls = dining_hall_scraper.scrape()
    for key in dining_halls.keys():
        dining_hall_dates = db.collection(u'Dining Halls and Cafes').document("Dining Halls").collection(str(key))

        for dining_hall in dining_halls[key].keys():
            dining_hall_dates.document(dining_hall).set(dining_halls[key][dining_hall])

def scrape_cafe_information():
    '''
        Run the cafe scraper and updates Firebase with new data
    '''
    from scrapers.dining import cafe_scraper
    cafe = cafe.CafeScraper()
    cafes = cafe.scrape()
    for key in cafes.keys():
        db.collection(u'Dining Halls and Cafes').document(key).set(cafes[key])

def scrape_library_information():
    '''
        Runs the library scrapers and updates Firebase with new data 
    '''
    from scrapers.libraries import library_scraper
    from scrapers.libraries import moffit_scrapper
    lib_scraper = library_scraper.LibraryScraper()
    libraries = lib_scraper.scrape()
    moffitt = moffit_scrapper.scrapper()
    # Adds moffitt to the libraries dictionary 
    libraries.update(moffitt) 
    
    # insert testing here 

    for library in libraries.keys():
        # integration_test.test_libraries(library)
    
        # this is the libraries in firebase
        db.collection(u'Libraries').document(library).set(libraries[library])


# def scrape_gym_information():
#     gyms = post_processor.process_gyms()
#     gyms_ref = db.collection("Gyms")
#     for resource in gyms:
#         resource.pop("id", None)
#         resource.pop("close", None)
#         resource.pop("open", None)
#         resource.pop("open_hours", None)
#         resource.pop("close_hours", None)

#         gym_ref = gyms_ref.document(u'{}'.format(resource["name"]))
#         gym_ref.set(resource)

# def scrape_gym_classes_information():
#     os.chdir(os.pardir)
#     try:
#         os.system("python3 scrapers/gyms/gym_classes.py")
#         shutil.move("gym_class_data.json", "firebase/gym_class_data.json")
#     except:
#         print("Error")

#     # Gym Classes Data
#     data_path = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "gym_class_data.json")

#     with open(data_path) as handle:
#         dictdump = json.loads(handle.read())

#         gyms_ref = db.collection("Gyms")

#         day, week_of_day, week_of_mon = helper.get_last_sunday()

#         gym_ref = gyms_ref.document(u'{}'.format("Gym Classes"))
        

#         for key in dictdump.keys():
#             gym_day_ref = gym_ref.collection(u'{}'.format(day))

#             index = 0
#             for c in dictdump[key]:
#                 gym_day_ref.document(u'{}'.format(index)).set(c)
#                 index += 1

#             day += datetime.timedelta(days=1)

'''
    Running scrapers and pushing to firebase 
'''
print("Updating Dining Hall Information...")
scrape_dining_hall_information()

print("Updating Cafe Information...")
scrape_cafe_information()

print("Updating Library Information...")
scrape_library_information()

# print("Scraping Gyms Information...")
# scrape_gym_information()

# print("Scraping Gym Classes Information...")
# scrape_gym_classes_information()