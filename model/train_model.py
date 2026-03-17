import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

# Get current directory (model folder)
current_dir = os.path.dirname(__file__)

# Path to dataset
data_path = os.path.join(current_dir, '..', 'data', 'students.csv')

# Load dataset
data = pd.read_csv(data_path)

# Features and target
X = data[['study_hours', 'attendance', 'assignments']]
y = data['grade']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model inside model folder
model_path = os.path.join(current_dir, 'model.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")