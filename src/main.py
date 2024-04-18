import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

HOME_PATH = "../"
DATA_PATH = "../Data/Participant_Data/"



def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"Error: Creating Directory with name : {path}")

def read_data(path):
    data = pd.read_csv(path)
    return data


def clean_data(data):
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
   
    columns = data.columns.tolist()
    for column in columns:
        flag = normalize_data(data,column)
        if(flag):
            # data = data.drop(columns=['time','poorSignalLevel','blinkStrength'])
            continue
    return data

def plot_data(data,PATH):
    columns = data.columns.tolist()
    # print(f"Columns : {columns}")
    # plt.figure(figsize=(20, 10))
    for column in columns:
        print(f"Plotting {column} with shape : {data[column].shape}\n")
        FILENAME = PATH+"_"+column
        # print(data.head())
        time = data['time']
        # print(f"Plotting {FILENAME} with shape : {data[column].shape} and time : {time.shape}\n")
        plt.plot(time,data)
        plt.xlabel("Time")
        plt.ylabel(column)
        plt.legend(data.columns.tolist())
        plt.title(FILENAME)
        create_dir(HOME_PATH + "Plots/" + PATH)
        # print(HOME_PATH + "Plots/"+ PATH + "/" + FILENAME + ".png")
        plt.savefig(HOME_PATH + "Plots/"+ PATH + "/" + FILENAME + ".png",dpi=300)
        plt.close()
        break
        

def normalize_data(data, column_name):
    scatter_data = data[column_name]
    normalized_data = (scatter_data - scatter_data.mean())/scatter_data.std()
    data[column_name] = normalized_data
    # print(f"Normalized {column_name} with shape : {normalized_data.shape}\n")
    return True

def main():
    Data = glob.glob(DATA_PATH + "*")
    for dataset in Data:
        PATH = dataset.split("/")[-1].split(".")[0]
        data = read_data(dataset)
        
        data_cleaned = clean_data(data)
        # print(f"Processing {PATH} : Shape of Data : {data_cleaned.shape}\n==============\n")
        try:
            plot_data(data_cleaned,PATH)
        except Exception as e:
            print(f"Error in Plotting : {e}")
            break
        break



if __name__ == "__main__":
    main()
