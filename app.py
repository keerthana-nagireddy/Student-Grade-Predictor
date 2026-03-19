from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

import os

model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

# Store history
history = []

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction page
@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')

# Predict
@app.route('/predict', methods=['POST'])
def predict():
    study_hours = float(request.form['study_hours'])
    attendance = float(request.form['attendance'])
    assignments = float(request.form['assignments'])

    result = model.predict([[study_hours, attendance, assignments]])

    # Save history
    history.append({
        "study_hours": study_hours,
        "attendance": attendance,
        "assignments": assignments,
        "grade": result[0]
    })

    return render_template('result.html', prediction=result[0])

# History page
@app.route('/history')
def history_page():
    return render_template('history.html', history=history)


if __name__ == "__main__":
    app.run()