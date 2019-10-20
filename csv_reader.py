#Load Pandas libraries
import pandas as pd


def read_csv():
    #Read data from file "resources.csv"
    data = pd.read_csv("/csv_data/resources.csv")
    data.head()

if __name__ == "__main__":
    read_csv