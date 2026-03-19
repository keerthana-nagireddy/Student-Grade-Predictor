from flask import Flask, render_template, request, session
import pickle
import os
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session

# Load model once (GOOD)
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
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
    # Assign unique user_id if not exists
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

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

    # Predict
    result = model.predict([[study_hours, attendance, assignments]])
    grade = result[0]

    # Save to DB with user_id
    user_id = session.get('user_id')

    conn = sqlite3.connect('database.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (user_id, study_hours, attendance, assignments, grade) VALUES (?, ?, ?, ?, ?)",
        (user_id, study_hours, attendance, assignments, grade)
    )
    conn.commit()
    conn.close()

    return render_template('result.html', prediction=grade)

# History page (ONLY current user data)
@app.route('/history')
def history_page():
    user_id = session.get('user_id')

    conn = sqlite3.connect('database.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT study_hours, attendance, assignments, grade 
        FROM history 
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "study_hours": row[0],
            "attendance": row[1],
            "assignments": row[2],
            "grade": row[3]
        })

    return render_template('history.html', history=history)


# IMPORTANT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)