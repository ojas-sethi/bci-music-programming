import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# Function to perform epoching on EEG data
def epoch_data(data, window_size=2):
    # Calculate the number of epochs based on the maximum time and window size
    max_time = data['time'].max()
    num_epochs = int(np.ceil(max_time / window_size))
    
    # Create a new column for the epoch number
    data['epoch'] = (data['time'] // window_size).astype(int)
    
    # Aggregate data by epochs, taking the mean of the EEG features within each epoch
    epoch_features = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']
    epoch_data = data.groupby('epoch')[epoch_features + ['label']].mean().reset_index()
    print(epoch_data.head())

    return epoch_data

# Load the data
data = pd.read_csv('combined_epoched_data.csv')

# Apply epoching
# data = epoch_data(data, window_size=2)

# Select the features and the label
features = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']
X = data[features]
y = data['label'].round().astype(int)

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.20, random_state=42)

# Initialize and train the SVM classifier
svm_model = SVC(kernel='rbf')
svm_model.fit(X_train, y_train)

# Predicting the labels on the test dataset
y_pred = svm_model.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", classification_rep)
