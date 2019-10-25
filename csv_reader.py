#Load Pandas libraries
import pandas as pd


def read_csv():
    #Read data from file "resources.csv"
    data = pd.read_csv("csv_data/resources.csv")
    for row in data.iterrows():
        for i in range(18):
            print(row[1][i])

if __name__ == "__main__":
    read_csv()