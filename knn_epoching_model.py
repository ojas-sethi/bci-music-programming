import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import BaggingClassifier
import joblib

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
data = pd.read_csv('combined_data.csv')
data = epoch_data(data, window_size=2)  # Including the epoching function

# Features and Labels
features = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']
X = data[features]
y = data['label'].round().astype(int)  # Ensuring labels are integers

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, 'scaler.pkl')

# SMOTE for balancing the dataset
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.40, random_state=42)

# KNN with Bagging
knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
bagging_model = BaggingClassifier(knn, n_estimators=50, random_state=42)
bagging_model.fit(X_train, y_train)

# Predict and Evaluate
y_pred = bagging_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model
joblib.dump(bagging_model, 'knn_epoched_model.pkl')
print("Model saved successfully!")
