import requests
import bs4 as bs

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

print(len(library_names))
print(len(library_urls))
print(library_to_url)
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
