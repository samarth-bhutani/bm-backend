from os.path import dirname, abspath
import os, json, pandas as pd

def scrape():
    '''
        Reads in the data from the resources csv and outputs a dictionary with the values
    '''
    #Read data from file "resources.csv"
    parent_working_directory = os.path.dirname((abspath(__file__)))

    data =  pd.read_csv(parent_working_directory + "/csv_data/latitude_longitudes.csv")

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

print(scrape())