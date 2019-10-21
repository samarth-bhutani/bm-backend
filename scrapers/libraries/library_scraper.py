import requests
from bs4 import BeautifulSoup as bs
import time 
import json

libraries = {}
library_names = ["Anthropology Library", "Art History/Classics Library", "BAMPFA Film Library & Study Center", "Bancroft Library/University Archives", "Berkeley Law Library", "Bioscience, Natural Resources & Public Health Library", "Business Library", "Career Counseling Library",
"CED Visual Resources Center", "Chemistry and Chemical Engineering Library", "Doe Library", "Earth Sciences & Map Library", "East Asian Library", "Engineering Library", "Environmental Design Library", "Ethnic Studies Library", "Graduate Theological Union Library", "Institute of Governmental Studies Library", "Institute of Transportation Studies Library", "Main (Gardner) Stacks", "Mathematics Statistics Library", "Moffitt Library", "Morrison Library", "Music Library", "Newspapers & Microforms Library", "Optometry and Health Sciences Library", "Physics-Astronomy Library", "Robbins Collection Library", "Social Research Library", "South/Southeast Asia Library"]
library_urls = ["http://www.lib.berkeley.edu/libraries/anthropology-library",
                "http://www.lib.berkeley.edu/libraries/art-history-classics-library", "http://www.lib.berkeley.edu/libraries/bampfa-library",
                "http://www.lib.berkeley.edu/libraries/bancroft-library", "http://www.lib.berkeley.edu/libraries/law-library", "http://www.lib.berkeley.edu/libraries/bioscience-library", "http://www.lib.berkeley.edu/libraries/business-library", "http://www.lib.berkeley.edu/libraries/career-counseling-library", "http://www.lib.berkeley.edu/libraries/visual-resources-center", "http://www.lib.berkeley.edu/libraries/chemistry-library", "http://www.lib.berkeley.edu/libraries/doe-library", "http://www.lib.berkeley.edu/libraries/earth-sciences-library", "http://www.lib.berkeley.edu/libraries/east-asian-library", "http://www.lib.berkeley.edu/libraries/engineering-library", "http://www.lib.berkeley.edu/libraries/environmental-design-library", "http://www.lib.berkeley.edu/libraries/ethnic-studies-library", "http://www.lib.berkeley.edu/libraries/graduate-theological-union-library", "http://www.lib.berkeley.edu/libraries/igs-library", "http://www.lib.berkeley.edu/libraries/its-library", "http://www.lib.berkeley.edu/libraries/main-stacks", "http://www.lib.berkeley.edu/libraries/math-library", "http://www.lib.berkeley.edu/libraries/moffitt-library", "http://www.lib.berkeley.edu/libraries/morrison-library", "http://www.lib.berkeley.edu/libraries/music-library", "http://www.lib.berkeley.edu/libraries/newspaper-microform-library", "http://www.lib.berkeley.edu/libraries/optometry-library", "http://www.lib.berkeley.edu/libraries/physics-library", "http://www.lib.berkeley.edu/libraries/robbins-collection-library", "http://www.lib.berkeley.edu/libraries/social-research-library", "http://www.lib.berkeley.edu/libraries/ssea-library"]
library_to_url = {}
#Initializing libraries dictionary
for i in range(len(library_names)):
    library = library_names[i]
    libraries[library] = {}
    library_to_url[library] = library_urls[i]

def set_library_ids(libraries):
    '''
    Sets library id in the libraries dictionary. 
    libraries[id] = int 
    Hardcoded because the JSON api arbitrarily assigns library ids. 
    '''
    libraries["Anthropology Library"]["id"] = 194
    libraries["Art History/Classics Library"]["id"] = 183
    libraries["BAMPFA Film Library & Study Center"]["id"] = 251
    libraries["Bancroft Library/University Archives"]["id"] = 196
    libraries["Berkeley Law Library"]["id"] = 242
    libraries["Bioscience, Natural Resources & Public Health Library"]["id"] = 198
    libraries["Business Library"]["id"] = 200
    libraries["Career Counseling Library"]["id"] = 259
    libraries["CED Visual Resources Center"]["id"] = 228
    libraries["Chemistry and Chemical Engineering Library"]["id"] = 202
    libraries["Doe Library"]["id"] = 173
    libraries["Earth Sciences & Map Library"]["id"] = 204
    libraries["East Asian Library"]["id"] = 206 
    libraries["Engineering Library"]["id"] = 210
    libraries["Environmental Design Library"]["id"] = 212
    libraries["Ethnic Studies Library"]["id"] = 232
    libraries["Graduate Theological Union Library"]["id"] = 249
    libraries["Institute of Governmental Studies Library"]["id"] = 236
    libraries["Institute of Transportation Studies Library"]["id"] = 240
    libraries["Main (Gardner) Stacks"]["id"] = 179 
    libraries["Mathematics Statistics Library"]["id"] = 214
    libraries["Moffitt Library"]["id"] = 179
    libraries["Morrison Library"]["id"] = 200
    libraries["Music Library"]["id"] = 216
    libraries["Newspapers & Microforms Library"]["id"] = 191
    libraries["Optometry and Health Sciences Library"]["id"] = 218
    libraries["Physics-Astronomy Library"]["id"] = 220
    libraries["Robbins Collection Library"]["id"] = 261
    libraries["Social Research Library"]["id"] = 224
    libraries["South/Southeast Asia Library"] = 192

def scrape_library_hours(libraries): 
    '''
    Scrapes library hours from library urls and stores it into the libraries dictionary.
    '''
    # testing one thing
    # anthro_lib = libraries[0]
    # library_url = library_to_url[anthro_lib]
    try:
        library_page = requests.get("http://www.lib.berkeley.edu/hours/api/libraries/194?begin_date=2019-10-27&end_date=2019-11-02")
        print(library_page.content)
    except Exception:
        print("Exception has occurred.")
    # soup = bs(library_page.content, "html.parser")

    
    # try:

    # except: 
    #     print("Error")


#page.content is how to get html 

"""
Hours is an array of: (datetime object, open time, close time)
Ex: (datetime object, 1pm, 5:30pm)

Get last Sunday

Hardcode dates into URLs for libraries 
or use specific library page itself:
http://www.lib.berkeley.edu/libraries/visual-resources-center

1. Iterate through list of libraries.
2. For each library:
    - Pull Sunday - Saturday data from library specific website
    - Create array of (datetime object, open time, close time)
    - Push to libraries dictionary
3. Push to JSON
"""

set_library_ids(libraries)
scrape_library_hours(library_names)
