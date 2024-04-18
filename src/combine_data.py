import pandas as pd

negative_data = pd.read_csv('NegativeTestData.csv')
neutral_data = pd.read_csv('NeutralTestData.csv')
positive_data = pd.read_csv('PositiveTestData.csv')

negative_data['Label'] = -1
neutral_data['Label'] = 0
positive_data['Label'] = 1

combined_data = pd.concat([negative_data, neutral_data, positive_data], ignore_index=True)

combined_data.to_csv('CombinedTestData.csv', index=False)

print("Data combined and saved successfully.")