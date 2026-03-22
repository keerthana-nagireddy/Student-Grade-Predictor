import pickle
import os

# 🔹 Recommendation logic
def get_recommendations(study_hours, attendance, assignments):
    recommendations = []

    if study_hours < 2:
        recommendations.append("Increase daily study time (at least 3-4 hours)")
    elif study_hours < 5:
        recommendations.append("Try to study more consistently")

    if attendance < 75:
        recommendations.append("Improve attendance to avoid missing important classes")

    if assignments < 5:
        recommendations.append("Complete assignments regularly")

    if not recommendations:
        recommendations.append("Excellent performance! Keep maintaining this consistency 💪")

    return recommendations


# 🔹 Prediction function
def predict_grade(study_hours, attendance, assignments):
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([[study_hours, attendance, assignments]])
    grade = prediction[0]

    recommendations = get_recommendations(study_hours, attendance, assignments)

    return grade, recommendations