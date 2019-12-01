from os import system
import json

class GymScraper:
    def scrape(self):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))

        system('scrapy runspider {}/gym_hours.py'.format(dir_path))
        system('python3 {}/gym_classes.py'.format(dir_path))

        gym_class_dict, gym_hours_dict = None, None

        with open('{}/gyms.json'.format(dir_path), 'r') as myfile:
            data = myfile.read()
            gym_hours_dict = (json.loads(data))

        with open('{}/gym_classes.json'.format(dir_path), 'r') as myfile:
            data = myfile.read()
            gym_class_dict = (json.loads(data))

        return gym_hours_dict, gym_class_dict


