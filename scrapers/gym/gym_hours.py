import scrapy
from scrapy.http.request import Request
from models import Gym
from geopy.geocoders import Nominatim

import os, sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from helper import *

import json

RSF_HOURS = 'https://recsports.berkeley.edu/rsf-hours/'
TRACK_HOURS = 'https://recsports.berkeley.edu/tracks/'
EDWARDS_TRACK = 'https://recsports.berkeley.edu/edwards-track/'
MEMORIAL_STADIUM_HOURS = 'https://recsports.berkeley.edu/stadium-fitness-center-hours/'
POOL_HOURS = 'https://recsports.berkeley.edu/lap-swim/'

gym_dict = dict()
geolocator = Nominatim()

class GymHoursSpider(scrapy.Spider):
    name = "gymHours"
    start_urls = ['https://recsports.berkeley.edu/']

    def parse(self, response):
        yield Request(url = RSF_HOURS, callback = self.parse_RSF)
        yield Request(url = TRACK_HOURS, callback = self.parse_track)
        yield Request(url = MEMORIAL_STADIUM_HOURS, callback = self.parse_memorial)
        yield Request(url = POOL_HOURS, callback = self.parse_pool)

    def parse_hour_string(self, hours):
        open_close = hours.split(" - ")
        if len(open_close) == 1:
            return "", ""
        else:
            return open_close[0], open_close[1]

    def parse_gym_facility_hours(self, response):
        # get hours for the next seven days, store in open and close lists
        hours = response.xpath('//main[contains(@class, "m-all t-2of3 d-5of7 cf col-md-8")]/article/section/div/table/tbody/tr/td/text()').extract()
        open_hours = list()
        close_hours = list()
        for x in range(14):
            if (x % 2 == 1):
                open_time, close_time = self.parse_hour_string(hours[x])
                open_hours.append(open_time)
                close_hours.append(close_time)
        # get description for facility
        description = response.xpath('//div[@id="extra-content-field"]/text()').extract()
        return description[0], open_hours, close_hours

    def parse_RSF(self, response):
        # get gym hours
        description, open, close = self.parse_gym_facility_hours(response)
        address = "2301 Bancroft Way, Berkeley, CA 94720"

        try:
	        lat = geolocator.geocode(address).latitude
	        long = geolocator.geocode(address).longitude
        except:
	        lat = 0
	        long = 0

        phone = "(510) 642-7796"
        image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Schedules-Facility-Hours.jpg"
        new_rsf = Gym("Recreational Sports Facility", lat, long, phone, image_url, description, address, open, close, True)
        gym_dict[new_rsf.name] = new_rsf
        self.output_file()

    def parse_memorial(self, response):
        # get gym hours
        description, open, close = self.parse_gym_facility_hours(response)
        address = "210 Stadium Rim Way, Berkeley, CA 94704"
        try:
	        lat = geolocator.geocode(address).latitude
	        long = geolocator.geocode(address).longitude
        except:
	        lat = 0
	        long = 0

        phone = "(510) 642-7796"
        image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Facilities-Stadium-Fitness-Center.jpg"
        new_memorial_stadium = Gym("Memorial Stadium", lat, long, phone, image_url, description, address, open, close, True)
        gym_dict[new_memorial_stadium.name] = new_memorial_stadium
        self.output_file()

    def parse_track(self, response):
        # get gym hours
        open, close = self.parse_track_hours(response)
        description = "Edwards Track is an eight-lane running track that is open for recreational use."
        address = "2223 Fulton St, Berkeley, CA 94704"
        try:
	        lat = geolocator.geocode(address).latitude
	        long = geolocator.geocode(address).longitude
        except:
	        lat = 0
	        long = 0

        phone = "(510) 642-7796"
        image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Facilities-Edwards-Track.jpg"
        new_edwards_track = Gym("Edwards Track", lat, long, phone, image_url, description, address, open, close, True)
        gym_dict["Edwards Track"] = new_edwards_track
        self.output_file()

    def parse_pool(self, response):
        # get gym hours
        open_dict, close_dict = self.parse_pool_hours(response)
        image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Schedules-Lap-Swim.jpg"
        phone = "(510) 642-7796"
        for pool in open_dict:
            open_hours = open_dict[pool]
            close_hours = close_dict[pool]
            address = ""
            if pool == "Hearst North Pool":
                address = "176 Hearst Ave, Berkeley, CA 94720"
                image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Facilities-Hearst-Gym-and-Pool.jpg"
                description = "Hearst Pool offers regular lap swim hours and includes amenities such as  locker rooms, hot showers, day locks, swim suit spinners, and towel service."
            elif pool == "GBRC Pool":
                address = "Sports Lane, Berkeley, CA 94705"
                image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Facilities-Golden-Bear-Rec.jpg"
                description = "The Golden Bear Recreation Center offers a pool, tennis courts, a track, and more, all on the Clark Kerr Campus."
            elif pool == "Spieker Pool":
                address = "2301 Bancroft Way, Berkeley, CA 94704"
                image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Facilities-Spieker-Pool.jpg"
                description = "The pool is 25 yards long with 18 lanes and water that is kept at 79-80 degrees F."
            elif pool == "SCRA Pool":
                # temp address fix, need to use lat/long
                address = "Strawberry Canyon Pool, Berkeley, CA 94704"
                image_url = "https://recsports.berkeley.edu/wp-content/uploads/2016/06/Facilities-SCRA.jpg"
                description = "Whether it’s in the seasonal pool or the thrilling ropes course, find your next adventure at Strawberry Canyon Recreation Area."
            try:
                lat = geolocator.geocode(address).latitude
                long = geolocator.geocode(address).longitude
            except:
                lat = 0
                long = 0

            new_pool = Gym(pool, lat, long, phone, image_url, description, address, open_hours, close_hours, True)
            gym_dict[pool] = new_pool
        self.output_file()
        # return new_edwards_track

    def parse_pool_hours(self, response):
        blocks = response.xpath('//main[contains(@class, "m-all t-2of3 d-5of7 cf col-md-8")]/article/section/div/table')
        pools = set()
        open_hours_dict = dict()
        close_hours_dict = dict()
        # add all pools to dictionary and set

        for b in blocks:
            hours = b.xpath('tbody/tr/td/text()').extract()
            for pool_name in range(len(hours)):
                if pool_name % 3 == 1:
                    open_hours_dict[hours[pool_name]] = []
                    close_hours_dict[hours[pool_name]] = []
                    pools.add(hours[pool_name])

        for b in blocks:
            open_dict = dict()
            close_dict = dict()
            for pool_name in pools:
                open_dict[pool_name] = []
                close_dict[pool_name] = []
            hours = b.xpath('tbody/tr/td/text()').extract()
            for h in range(len(hours)):
                if h % 3 == 0:
                    open_time, close_time = self.parse_hour_string(hours[h])
                    open_dict[hours[h + 1]].append(open_time)
                    close_dict[hours[h + 1]].append(close_time)
            for pool, hours_lst in open_dict.items():
                open_hours_dict[pool].append(hours_lst)
            for pool, hours_lst in close_dict.items():
                close_hours_dict[pool].append(hours_lst)
        return open_hours_dict, close_hours_dict

    def parse_track_hours(self, response):
        blocks = response.xpath('//main[contains(@class, "m-all t-2of3 d-5of7 cf col-md-8")]/article/section/div/table')
        open_hours = list()
        close_hours = list()
        for b in blocks:
            hours = b.xpath('tbody/tr/td/text()').extract()
            open_hours_of_day = list()
            close_hours_of_day = list()
            for h in range(len(hours)):
                if h % 3 == 0:
                    open_time, close_time = self.parse_hour_string(hours[h])
                    open_hours_of_day.append(open_time)
                    close_hours_of_day.append(close_time)
            open_hours.append(open_hours_of_day)
            close_hours.append(close_hours_of_day)
        return open_hours, close_hours

    def output_file(self):
        if (len(gym_dict) == 7):
            with open('gyms.json', 'w') as outfile:
                json.dump(gym_dict, outfile, default=lambda o: o.__dict__)
