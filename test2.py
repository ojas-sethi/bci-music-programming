import numpy as np
import pandas as pd
import sys
import json
import time
from telnetlib import Telnet

# Initializing the columns for the CSV file
columns = [
    'time', 'attention', 'meditation', 'delta', 'theta', 'lowAlpha', 'highAlpha',
    'lowBeta', 'highBeta', 'lowGamma', 'highGamma', 'blinkStrength', 'poorSignalLevel'
]
data = {col: [] for col in columns}

# Start timer
start = time.perf_counter()

# Setting up the Telnet connection
tn = Telnet('localhost', 13854)
tn.write('{"enableRawOutput": false, "format": "Json"}'.encode('utf-8'))

try:
    with open('eeg_data.csv', 'w') as file:
        # Write the header row
        file.write(','.join(columns) + '\n')
        
        while True:
            line = tn.read_until(b'\r')
            print(line)  # Print the raw JSON line to the console
            decoded_line = line.decode('utf-8').strip()
            
            try:
                # Parse JSON and extract data
                json_data = json.loads(decoded_line)
                
                if "eSense" in json_data and "eegPower" in json_data:
                    esense = json_data['eSense']
                    eeg_power = json_data['eegPower']
                    poor_signal_level = json_data['poorSignalLevel']
                    
                    # Extracting individual values
                    attention = esense['attention']
                    meditation = esense['meditation']
                    delta = eeg_power['delta']
                    theta = eeg_power['theta']
                    low_alpha = eeg_power['lowAlpha']
                    high_alpha = eeg_power['highAlpha']
                    low_beta = eeg_power['lowBeta']
                    high_beta = eeg_power['highBeta']
                    low_gamma = eeg_power['lowGamma']
                    high_gamma = eeg_power['highGamma']
                    
                    # Current time since the script start
                    current_time = time.perf_counter() - start
                    
                    # Storing data
                    row_data = [
                        str(current_time), str(attention), str(meditation), str(delta),
                        str(theta), str(low_alpha), str(high_alpha), str(low_beta),
                        str(high_beta), str(low_gamma), str(high_gamma), str('0'),  # Assuming blinkStrength is not provided
                        str(poor_signal_level)
                    ]
                    
                    # Writing data to the CSV file
                    file.write(','.join(row_data) + '\n')
                
                # Optionally, sleep to prevent too much data from being written too quickly
                time.sleep(1)
                
            except json.JSONDecodeError:
                # Handle possible json decoding error
                print("Failed to decode:", decoded_line)
except Exception as e:
    print("An error occurred:", e)
finally:
    tn.close()
