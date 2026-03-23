from flask import Flask, render_template, request, session
import sqlite3
import uuid
import os

from model.predict import predict_grade, suggest_improvement

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------------- DATABASE ----------------------
def get_connection():
    return sqlite3.connect('database.db', timeout=10)


def init_db():
    conn = get_connection()
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


# ---------------------- ROUTES ----------------------

@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')


@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')


# 🔥 PREDICT WITH VALIDATION + FIXED LOGIC
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 🔹 Safe input parsing
        study_hours = float(request.form.get('study_hours', '').strip())
        attendance = float(request.form.get('attendance', '').strip())
        assignments = float(request.form.get('assignments', '').strip())

        # 🔥 VALIDATION
        if study_hours < 0 or attendance < 0 or assignments < 0:
            return render_template('predict.html', error="❌ Values cannot be negative")

        if attendance > 100:
            return render_template('predict.html', error="❌ Attendance cannot exceed 100%")

        if study_hours > 24:
            return render_template('predict.html', error="❌ Study hours cannot exceed 24")

        if assignments > 10:
            return render_template('predict.html', error="❌ Assignments must be between 0 and 10")

        # 🔹 Prediction
        grade, recommendations = predict_grade(study_hours, attendance, assignments)

        # 🔥 ✅ FIXED LOGIC HERE
        if grade == "A":
            recommendations = "🌟 Good! Keep it up with your efforts 💪"
            improvement_tip = None
        else:
            improvement_tip = suggest_improvement(study_hours, attendance, assignments)

        # 🔹 Save to DB
        user_id = session.get('user_id')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (user_id, study_hours, attendance, assignments, grade) VALUES (?, ?, ?, ?, ?)",
            (user_id, study_hours, attendance, assignments, grade)
        )
        conn.commit()
        conn.close()

        # 🔥 Send everything to frontend
        return render_template(
            'result.html',
            prediction=grade,
            recommendations=recommendations,
            improvement=improvement_tip
        )

    except ValueError:
        return render_template('predict.html', error="❌ Please enter valid numeric values")

    except Exception as e:
        print("Error:", e)
        return render_template('predict.html', error="❌ Something went wrong")


@app.route('/history')
def history_page():
    user_id = session.get('user_id')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT study_hours, attendance, assignments, grade 
        FROM history 
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "study_hours": row[0],
            "attendance": row[1],
            "assignments": row[2],
            "grade": row[3]
        }
        for row in rows
    ]

    return render_template('history.html', history=history)


# ---------------------- RUN ----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)