import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.svm import SVC

# Custom normalization function
def normalize_data(data, column_name):
    scatter_data = data[column_name]
    normalized_data = (scatter_data - scatter_data.mean()) / scatter_data.std()
    data[column_name] = normalized_data
    return True

# Load the data
data = pd.read_csv('combined_data.csv')

# Select the features and the label
features = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']
for feature in features:
    normalize_data(data, feature)

X = data[features]
y = data['label']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Parameters for Randomized Search
parameters = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.01, 0.1, 1, 10],
    'kernel': ['linear', 'rbf', 'poly'],
    'class_weight': ['balanced', None]
}

svm = SVC()
random_search = RandomizedSearchCV(svm, parameters, n_iter=10, cv=5, scoring='accuracy', verbose=2, random_state=42, n_jobs=-1)
random_search.fit(X_train, y_train)

print("Best parameters found: ", random_search.best_params_)
best_svm = random_search.best_estimator_

# Predicting the labels on the test dataset
y_pred = best_svm.predict(X_test)

# Evaluate the model's performance
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
