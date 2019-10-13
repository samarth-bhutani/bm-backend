import requests
import bs4 as bs
import pandas as pd
import os.path

libraries = {}
libraries["Anthropology Library"] = {}
libraries["Art History/Classics Library"] = {}
libraries["BAMPFA Film Library & Study Center"] = {}
libraries["Bancroft Library/University Archives"] = {}
libraries["Berkeley Law Library"] = {}
libraries["Bioscience, Natural Resources & Public Health Library"] = {}
libraries["Business Library"] = {}
libraries["Career Counseling Library"] = {}
libraries["CED Visual Resources Center"] = {}
libraries["Chemistry and Chemical Engineering Library"] = {}
libraries["Doe Library"] = {}
libraries["Earth Sciences & Map Library"] = {}
libraries["East Asian Library"] = {}
libraries["Engineering Library"] = {}
libraries["Environmental Design Library"] = {}
libraries["Ethnic Studies Library"] = {}
libraries["Graduate Theological Union Library"] = {}
libraries["Institute of Governmental Studies Library"] = {}
libraries["Institute of Transportation Studies Library"] = {}
libraries["Main (Gardner) Stacks"] = {}
libraries["East Asian Library"] = {}
libraries["Engineering Library"] = {}
libraries["East Asian Library"] = {}
libraries["Engineering Library"] = {}
libraries["East Asian Library"] = {}
libraries["Engineering Library"] = {}

"""
Hours is an array of: (datetime object, open time, close time)
Ex: (datetime object, 1pm, 5:30pm)

Get last Sunday

Hardcode dates into URLs for libraries 


"""