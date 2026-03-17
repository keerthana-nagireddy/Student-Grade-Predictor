import pickle
import os

def predict_grade(study_hours, attendance, assignments):
    # Get current directory
    current_dir = os.path.dirname(__file__)

    # Load model path
    model_path = os.path.join(current_dir, 'model.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([[study_hours, attendance, assignments]])
    return prediction[0]


# Test
print(predict_grade(8, 90, 9))