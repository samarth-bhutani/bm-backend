#Load Pandas libraries
import json
import pandas as pd


## read_csv will read data from a csv file and output it into json format.
## Author: Kevin Liu, Last Update 10/26/19
def read_csv():

    #Read data from file "resources.csv"
    data = pd.read_csv("csv_data/resources.csv")

    #Extract column names
    fields = data.columns.values

    #Make master array to store each resource, each item in resource is of type dictionary.
    list_of_resources = []

    #Loop through each row in csv
    for row in data.iterrows():
        new_resource = {}
        #Loop through each column for each row.
        for i in range(18):
            new_resource[fields[i]] = row[1][i]
        list_of_resources.append(new_resource)

    #Write to json file    
    with open('resources.txt', 'w') as json_file:
        for i in list_of_resources:
            json.dump(i,json_file, indent = 4, sort_keys = False)

##Testing
# if __name__ == "__main__":
#     read_csv()