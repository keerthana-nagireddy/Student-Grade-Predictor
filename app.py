from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load trained model
model = pickle.load(open('model.pkl', 'rb'))

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    study_hours = float(request.form['study_hours'])
    attendance = float(request.form['attendance'])
    assignments = float(request.form['assignments'])

    # Make prediction
    result = model.predict([[study_hours, attendance, assignments]])

    return render_template('result.html', prediction=result[0])

# Run app
if __name__ == "__main__":
    app.run(debug=True)