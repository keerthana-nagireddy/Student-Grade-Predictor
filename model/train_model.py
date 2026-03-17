import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

import os

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'data', 'students.csv')

data = pd.read_csv(file_path)

# Select features and target
X = data[['study_hours', 'attendance', 'assignments']]
y = data['grade']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")