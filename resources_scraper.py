from os.path import dirname, abspath
import os, json, pandas as pd, re
import helper


def scrape():
    '''
        Reads in the data from the resources csv and outputs a dictionary with the values
    '''
    #Read data from file "resources.csv"
    parent_working_directory = os.path.dirname((abspath(__file__)))

    data =  pd.read_csv(parent_working_directory + "/csv_data/resources.csv")

    #Extract column names
    fields = data.columns.values

    #Make master array to store each resource, each item in resource is of type dictionary.

    #Loop through each row in csv
    all_resources = {}
    for category in data["category"].unique():
        if len(category.strip()) == 0:
            continue

        category_resources = {}
        for row in data[data["category"] == category].iterrows():
            new_resource = {}

            #Loop through each column for each row.
            for i in range(18):
                new_resource[fields[i]] = row[1][i]

            # Collapsing monday_hours .... sunday_hours and converting to interval
            intervals = []
            dates = helper.get_this_week_dates()
            hours_df_key = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

            for day, date in zip(hours_df_key, dates): 
                csv_read = new_resource["{}_hours".format(day)]
                if str(csv_read) != "nan":                    
                    for time in csv_read.split(","):
                        if not bool(re.search(r'\d', time)):
                            intervals.append(helper.build_time_interval(open="Closed", close="Closed", date=date))
                        else:
                            time = time.split("-")
                            open = helper.standarize_timestring(time[0])
                            close = helper.standarize_timestring(time[1])
                            intervals.append(helper.build_time_interval(open=open, close=close, date=date))
                                
                if isinstance(new_resource["by_appointment"], str) and "Yes" in new_resource["by_appointment"]:
                    new_resource["by_appointment"] = True
                elif isinstance(new_resource["by_appointment"], str):
                    new_resource["by_appointment"] = False

                if isinstance(new_resource["on_campus"], str) and "Yes" in new_resource["on_campus"]:
                    new_resource["on_campus"] = True
                elif isinstance(new_resource["on_campus"], str):
                    new_resource["on_campus"] = False

                del new_resource["{}_hours".format(day)]
            
            new_resource["open_close_array"] = intervals
            category_resources[new_resource['name']] = new_resource

        all_resources[category] = category_resources

    return all_resources
