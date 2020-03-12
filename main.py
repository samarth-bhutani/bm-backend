import cafe_scraper, dining_hall_scraper, library_scraper, moffitt_scraper, firebase_push
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
    
    bucket_name = "bm-backend_scrap"
    destination_blob_name = "output.json"
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(str(scraped))

def scrape_and_push(request):
    """
        Runs all the scrapers and pushes the data to Firebase. 
    """