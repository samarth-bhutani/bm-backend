import cafe_scraper, dining_hall_scraper, library_scraper, moffitt_scraper, firebase_push
import firebase_admin, os, sys, shutil, inspect, json, pandas as pd, datetime
from firebase_admin import credentials, firestore
from google.cloud import storage

def scrape_all(request):
    print(request)
    cafes = cafe_scraper.scrape()
    dining_halls = dining_hall_scraper.scrape()
    libraries = library_scraper.scrape()

    scraped = {}
    scraped.update(cafes)
    scraped.update(dining_halls)
    scraped.update(libraries)
    print(scraped)
    
    '''
        For logging purposes 
    '''
    bucket_name = "bm-backend_scrap"
    destination_blob_name = "output.json"
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(str(scraped))

def scrape_and_push(request):
    '''
        Runs all the scrapers and pushes the data to Firebase. 
    '''
    db = firebase_push.update_credentials()
    firebase_push.log_time(db)
    # print("Updating dining halls...")
    # firebase_push.scrape_dining_hall_information(db)
    # print("Dining hall update complete!")

    # print("Updating cafes...")
    # firebase_push.scrape_cafe_information(db)
    # print("Cafe update complete!")
    
    print("Updating libraries...")
    firebase_push.scrape_library_information(db)
    print("Libraries update complete!")
    
    print("Updating resources...")
    firebase_push.scrape_resources_information(db)
    print("Resources update complete!")
    
    print("Updating events...")
    firebase_push.scrape_events_information(db)
    print("Events update complete!")

    # print("Updating gyms...")
    # firebase_push.scrape_gym_information(db) 
    # print("Gym update complete!")

    # print("Updating gym classes...")
    # firebase_push.scrape_gym_information(db) 
    # print("Gym class update complete!")
