from flask import Flask, render_template, request
import pickle
import os
import sqlite3

app = Flask(__name__)

# Load model safely
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_hours REAL,
            attendance REAL,
            assignments REAL,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
    grade = result[0]

    # Save to DB
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (study_hours, attendance, assignments, grade) VALUES (?, ?, ?, ?)",
        (study_hours, attendance, assignments, grade)
    )
    conn.commit()
    conn.close()

    return render_template('result.html', prediction=grade)

# History page
@app.route('/history')
def history_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT study_hours, attendance, assignments, grade FROM history")
    rows = cursor.fetchall()
    conn.close()

    # Convert to list of dicts
    history = []
    for row in rows:
        history.append({
            "study_hours": row[0],
            "attendance": row[1],
            "assignments": row[2],
            "grade": row[3]
        })

    return render_template('history.html', history=history)


if __name__ == "__main__":
    app.run()