import requests
from bs4 import BeautifulSoup
import time
from  geopy.geocoders import Nominatim
import spacy
import en_core_web_sm 
#YOU MUST INCLUDE THIS LINE FOR SPACY MODEL IN requirements.txt for cloud deployment
#https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz#en_core_web_sm
#(model and spacy version must also match)

from firebase_admin import credentials, firestore

def update_credentials():
    '''
        Updates credentials and returns a firestore client 
        On cloud functions you don't need to call initialize app or use credentials
    '''
    # for cloud-function pushing 

    db = firestore.Client()
    return db 

def twitter_scrape(db, url):
    '''
    PART I: Scrape Tweets from Twitter
    '''
    res = requests.get(url)
    html = BeautifulSoup(res.text, 'html.parser')
    tweets = {}
    timeline = html.select('#timeline li.stream-item')

    for tweet in timeline:

        tweet_id = tweet['data-item-id']
        tweet_epoch_time = tweet.select('a.tweet-timestamp')[0].find("span")['data-time']
        #tweet_pretty_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(int(tweet_epoch_time)))
        tweet_pretty_date = time.strftime('%Y-%m-%d', time.localtime(int(tweet_epoch_time)))
        tweet_pretty_time = time.strftime('%H-%M-%S', time.localtime(int(tweet_epoch_time)))
        tweet_text = tweet.select('p.tweet-text')[0].get_text()

        '''
        PART II: Use NLP to Determine Contextual Keywords
        '''
        nlp = en_core_web_sm.load()
        doc = nlp(tweet_text)
        keywords = []
        for token in doc.ents:
            if token.label_ in ['GPE', 'FAC', 'LOC']:
                if ":" not in token.text:
                    keywords.append((token.text,token.label_))

        '''
        PART III: Query Location Data
        '''
        geolocator = Nominatim()
        query_text = ""
        loc = None

        for keyword,label in keywords:
            query_text+=" "+keyword
        query_text+=", Berkeley" #sample query text looks like People's Park, Berkeley
        
        if query_text != ", Berkeley":
            loc = geolocator.geocode(query_text)

        if loc:
            #print("https://www.google.com/search?q="+str(loc.latitude)+"%2C+"+str(loc.longitude))
            lat = loc.latitude
            lon = loc.longitude
        else: #default to UC Berkley
            lat = 37.8719
            lon = -122.2585
        

        tweets[tweet_pretty_time] = {"time" : tweet_epoch_time, "id" : tweet_id, "text" : tweet_text, "lat": lat, "lon": lon}

        
        #tweets_document = db.collection(u'UCPD Tweets').document(tweet_pretty_time)
        tweets_document = db.collection(u'UCPD Tweets').document(tweet_pretty_date).collection(u'Tweets').document(tweet_pretty_time)
        tweets_document.set(tweets[tweet_pretty_time])

    return tweets

def run(req):
    db = update_credentials()
    UCPD_URL = 'https://twitter.com/UCPD_Cal'
    tweets = twitter_scrape(db, UCPD_URL)
    print(tweets)
