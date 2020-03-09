#Load Pandas libraries
import json
import pandas as pd
import os


class ResourcesScraper:
    def scrape(self):

        #Read data from file "resources.csv"
        path = os.path.dirname(__file__).split('/')[:-2]
        pathS = ""

        for p in path:
            pathS += p + '/'

        data = pd.read_csv(pathS+"csv_data/resources.csv")

        #Extract column names
        fields = data.columns.values

        #Make master array to store each resource, each item in resource is of type dictionary.

        #Loop through each row in csv
        all_resources = {}
        for category in data["category"].unique():
            category_resources = {}
            for row in data[data["category"] == category].iterrows():
                new_resource = {}
                #Loop through each column for each row.
                for i in range(18):
                    new_resource[fields[i]] = row[1][i]
                category_resources[new_resource['name']] = new_resource

            all_resources[category] = category_resources

        return all_resources