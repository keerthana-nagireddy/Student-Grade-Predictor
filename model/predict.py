import pickle
import os

# 🔥 Load model ONCE (global)
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)


# 🔹 Recommendation logic
def get_recommendations(study_hours, attendance, assignments, grade):
    recommendations = []

    if study_hours < 2:
        recommendations.append("Increase daily study time (at least 3-4 hours)")
    elif study_hours < 5:
        recommendations.append("Try to study more consistently")

    if attendance < 75:
        recommendations.append("Improve attendance to avoid missing classes")

    if assignments < 5:
        recommendations.append("Complete assignments regularly")

    # 🔥 NEW LOGIC
    if not recommendations:
        if grade in ['A']:
            recommendations.append("Excellent performance! Keep maintaining this consistency 💪")
        else:
            recommendations.append("You're doing well, but there’s room for improvement to reach Grade A 🚀")

    return recommendations

# 🔹 Prediction function
def predict_grade(study_hours, attendance, assignments):
    prediction = model.predict([[study_hours, attendance, assignments]])
    grade = prediction[0]

    recommendations = get_recommendations(study_hours, attendance, assignments, grade)
    return grade, recommendations

def suggest_improvement(study_hours, attendance, assignments):
    target = None

    # Try increasing study hours
    for h in range(int(study_hours), 25):
        grade, _ = predict_grade(h, attendance, assignments)
        if grade in ['A', 'A+']:
            target = f"Increase study hours to {h}"
            break

    # Try attendance if not found
    if not target:
        for a in range(int(attendance), 101):
            grade, _ = predict_grade(study_hours, a, assignments)
            if grade in ['A', 'A+']:
                target = f"Increase attendance to {a}%"
                break

    # Try assignments
    if not target:
        for ass in range(int(assignments), 11):
            grade, _ = predict_grade(study_hours, attendance, ass)
            if grade in ['A', 'A+']:
                target = f"Complete at least {ass} assignments"
                break

    if not target:
        target = "You're close! Improve all areas slightly to reach Grade A 🚀"

    return target