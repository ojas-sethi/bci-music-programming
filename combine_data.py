import pandas as pd

# List of filenames to combine
filenames = [
    'Data/CombinedTestData.csv', 'Data/NikhilNegative1.csv', 'Data/NikhilNegative2.csv',
    'Data/NikhilNeutral.csv', 'Data/NikhilPositive1.csv', 'Data/NikhilPositive2.csv',
    'Data/NitigyaNegative.csv', 'Data/NitigyaPositive.csv', 'Data/NitigyaNeutral.csv'
]

# Create a list to store the data from each file
dataframes = []

# Loop through the list of filenames
for filename in filenames:
    # Read each file into a DataFrame
    df = pd.read_csv(filename)
    # Append the DataFrame to the list
    dataframes.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)

print("All files have been successfully combined into combined_data.csv")