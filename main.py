import cafe_scraper, dining_hall_scraper, library_scraper, moffitt_scraper

def scrape_all():
    print(cafe_scraper.scrape())
    print(dining_hall_scraper.scrape())
    print(library_scraper.scrape())
    print(moffitt_scraper.scrape())

scrape_all()