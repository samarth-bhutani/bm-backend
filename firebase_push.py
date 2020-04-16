import firebase_admin, os, sys, shutil, inspect, json, pandas as pd, datetime
from os.path import dirname, abspath
from firebase_admin import credentials, firestore
import cafe_scraper, dining_hall_scraper, events_scraper, library_scraper, moffitt_scraper, resources_scraper, gym_scraper, gym_classes_scraper, helper
from datetime import datetime
import pytz
# from post_processing import post_processor
# from integration_test import Testing
# integration_test = Testing()

"""
    Helper functions
"""
def update_credentials():
    '''
        Updates credentials and returns a firestore client 

        On cloud functions you don't need to call initialize app or use credentials
    '''
    # for local pushing
    parent_working_directory = os.path.dirname((abspath(__file__)))
    cred = credentials.Certificate(parent_working_directory + "/berkeley-mobile-backend-firebase-key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # for cloud-function pushing 
    # db = firestore.Client()
    return db 

def scrape_dining_hall_information(db):    
    dining_halls = dining_hall_scraper.scrape()
    for dining_hall in dining_halls:
        menu = dining_halls[dining_hall].pop("menu")
        dining_hall_document = db.collection(u'Dining Halls').document(dining_hall)
        dining_hall_document.set(dining_halls[dining_hall])
        for date in menu: 
            date_ref = dining_hall_document.collection(str(date.date()))
            for meal in menu[date]:
                meal_doc = date_ref.document(meal)
                items = {"items": menu[date][meal]}
                meal_doc.set(items)

def scrape_cafe_information(db):
    '''
        Run the cafe scraper and updates Firebase with new data
    '''
    cafes = cafe_scraper.scrape()
    for key in cafes.keys():
        db.collection(u'Cafes').document(key).set(cafes[key])

def scrape_library_information(db):
    '''
        Runs the library scrapers and updates Firebase with new data 
    '''
    libraries = library_scraper.scrape()
    moffitt = moffitt_scraper.scrape()
    # # # Adds moffitt to the libraries dictionary 
    libraries["Moffitt Library"] = moffitt


    for library in libraries.keys():
        # edge cases: '/' char in name 
        name = library
        if library == "Art History/Classics Library": 
            name = "Art History and Classics Library" 
        elif library == "Bancroft Library/University Archives":
            name = "Bancroft Library and University Archives"  
        elif library == "South/Southeast Asia Library": 
            name = "South and Southeast Asia Library"
    
        try:
            lib_doc = db.collection(u'Libraries').document(name)
            lib_doc.set(libraries[library])
        except Exception as e:
            print(e)
            print(library)

def scrape_resources_information(db):
    '''
        Run the resources scraper and updates Firebase with new data
    '''
    resources = resources_scraper.scrape()
    for resource_types in resources:
        resource_collection = db.collection(str(resource_types))
        for resource in resources[resource_types]:
            resource_collection.document(str(resource)).set(resources[resource_types][resource])

def scrape_events_information(db):
    '''
        Runs the events scraper and updates Firebase with new data
    '''
    events = events_scraper.scrape()
    event_collection = db.collection(u'Events')
    for day in events.keys():
        event_collection.document(day).set(events[day])

def scrape_gym_information(db):
    '''
        Runs the gym scraper and updates Firebase with new data
    '''
    gyms = gym_scraper.scrape()
    gym_collection = db.collection(u'Gyms')
    for gym in gyms:
        gym_collection.document(gym["name"]).set(gym)

def scrape_gym_classes_information(db):
    '''
        Runs the gym classes scraper and updates Firebase with new data
    '''
    gym_classes = gym_classes_scraper.scrape()
    gym_classes_collection = db.collection(u'Gym Classes')
    for day in gym_classes:
        gym_classes_collection.document(day).set(gym_classes[day])

def log_time(db):
    '''
        Logs the last time firebase has been updated
    '''
    timezone = pytz.timezone("America/Los_Angeles")
    current = datetime.now(timezone)
    dt_string = current.strftime("%m/%d/%Y %H:%M:%S")
    dictionary = {} 
    dictionary["timestamp"] = dt_string
    db.collection(u'Logs').document("Last Updated").set(dictionary)
