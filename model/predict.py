import pickle
import os

# 🔹 Recommendation logic
def get_recommendations(study_hours, attendance, assignments):
    recommendations = []

    if study_hours < 2:
        recommendations.append("Increase daily study time (at least 3-4 hours)")

    elif study_hours < 5:
        recommendations.append("Try to study a little more consistently")

    if attendance < 75:
        recommendations.append("Improve attendance to avoid missing important classes")

    if assignments < 5:
        recommendations.append("Complete assignments regularly for better understanding")

    if not recommendations:
        recommendations.append("Excellent performance! Keep maintaining this consistency 💪")

    return recommendations


# 🔹 Main prediction function
def predict_grade(study_hours, attendance, assignments):
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([[study_hours, attendance, assignments]])
    grade = prediction[0]

    # Get recommendations
    recommendations = get_recommendations(study_hours, attendance, assignments)

    return grade, recommendations


# 🔹 Test
if __name__ == "__main__":
    grade, recs = predict_grade(8, 90, 9)
    print("Grade:", grade)
    print("Recommendations:", recs)