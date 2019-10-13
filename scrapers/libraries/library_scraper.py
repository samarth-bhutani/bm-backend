import requests
import bs4 as bs

libraries = {}
library_names = ["Anthropology Library", "Art History/Classics Library", "BAMPFA Film Library & Study Center", "Bancroft Library/University Archives", "Berkeley Law Library", "Bioscience, Natural Resources & Public Health Library", "Business Library", "Career Counseling Library",
"CED Visual Resources Center", "Chemistry and Chemical Engineering Library", "Doe Library", "Earth Sciences & Map Library", "East Asian Library", "Engineering Library", "Environmental Design Library", "Ethnic Studies Library", "Graduate Theological Union Library", "Institute of Governmental Studies Library", "Institute of Transportation Studies Library", "Main (Gardner) Stacks", "Mathematics Statistics Library", "Moffitt Library", "Morrison Library", "Music Library", "Newspapers & Microforms Library", "Optometry and Health Sciences Library", "Physics-Astronomy Library", "Robbins Collection Library", "Social Research Library", "South/Southeast Asia Library"]

library_urls = [] 

library_to_url = {}

#Initializing libraries dictionary 
for library in library_names:
    libraries[library] = {}

print(libraries)
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
