from scrapers.libraries.library_scraper import LibraryScraper
from scrapers.libraries.moffit_scrapper import MoffitLibraryScraper

from scrapers.gym.gym_scraper import GymScraper

from scrapers.dining.cafe_scraper import CafeScraper
from scrapers.dining.dining_hall_scraper import DiningHallScraper
from scrapers.resources.resources_scraper import ResourcesScraper

LibraryScraper().scrape()
MoffitLibraryScraper().scrape()
GymScraper().scrape()
CafeScraper().scrape()
DiningHallScraper().scrape()
ResourcesScraper().scrape()




