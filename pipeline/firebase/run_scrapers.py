import os
from pathlib import Path
import shutil

scrapers = ["scrapers/dining/cafe", "scrapers/dining/dining_hall", "scrapers/gym/gym_hours", "scrapers/gym/gym_classes"]

for scraper in scrapers:
    os.chdir(Path(os.getcwd()).parent)
    os.system("python3 {}_scraper.py".format(scraper))

    shutil.move("{}_.".format(scraper), "python3 {}_scraper.py".format(scraper))