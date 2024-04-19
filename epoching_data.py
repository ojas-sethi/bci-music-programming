import pandas as pd
import numpy as np

def epoch_data(data, window_size=2):
    # Calculate the number of epochs based on the maximum time and window size
    max_time = data['time'].max()
    num_epochs = int(np.ceil(max_time / window_size))
    
    # Create a new column for the epoch number
    data['epoch'] = (data['time'] // window_size).astype(int)
    
    # Features for aggregation
    epoch_features = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']
    
    # Aggregate data by mean within each epoch
    epoch_data = data.groupby('epoch')[epoch_features].mean().reset_index()
    
    return epoch_data

def process_files(file_info):
    combined_data = pd.DataFrame()  # Initialize empty DataFrame for combined results

    for info in file_info:
        # Load data from file
        data = pd.read_csv(info['filename'])
        
        # Apply epoching (without labels)
        epoched_data = epoch_data(data)
        
        # Assign the label to the entire epoch data
        epoched_data['label'] = info['label']
        
        # Append to the combined DataFrame
        combined_data = pd.concat([combined_data, epoched_data], ignore_index=True)
    
    return combined_data

# Example usage
file_info = [
    {'filename': 'Data/NikhilPositive1.csv', 'label': 1},
    {'filename': 'Data/NikhilPositive2.csv', 'label': 1},
    {'filename': 'Data/NikhilNeutral.csv', 'label': 0},
    {'filename': 'Data/NikhilNegative1.csv', 'label': -1},
    {'filename': 'Data/NikhilNegative2.csv', 'label': -1},
    {'filename': 'Data/NitigyaPositive.csv', 'label': 1},
    {'filename': 'Data/NitigyaNeutral.csv', 'label': 0},
    {'filename': 'Data/NitigyaNegative.csv', 'label': -1}
]

# Process the files and combine data
combined_data = process_files(file_info)
print(combined_data.head())

combined_data.to_csv('combined_epoched_data.csv', index=False)
print("Combined data saved to 'combined_epoched_data.csv'.")