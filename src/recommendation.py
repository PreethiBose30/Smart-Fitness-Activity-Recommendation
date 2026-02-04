# Fitness recommendation logic
def calculate_bmi(height, weight):
    return weight / (height * height)


def recommend_fitness(age, bmi, medical_condition, activity_level):
    recommendations = []
    notes = []

    # Medical condition check
    if medical_condition == "yes":
        recommendations.append("Walking")
        recommendations.append("Yoga")
        notes.append("Avoid high-intensity workouts")

    # BMI-based recommendations
    if bmi < 18.5:
        recommendations.append("Light strength training")
        notes.append("Focus on healthy weight gain")
    elif bmi < 25:
        recommendations.append("Jogging")
        recommendations.append("General fitness exercises")
    elif bmi < 30:
        recommendations.append("Brisk walking")
        notes.append("Gradual weight loss recommended")
    else:
        recommendations.append("Low-impact cardio")
        notes.append("Consult a fitness professional")

    # Activity level
    if activity_level == "active" and age < 30:
        recommendations.append("Strength training")

    return recommendations, notes


# Test the logic
if __name__ == "__main__":
    height = 1.65  # meters
    weight = 70    # kg
    age = 20
    activity_level = "beginner"
    medical_condition = "no"

    bmi = calculate_bmi(height, weight)
    recs, notes = recommend_fitness(age, bmi, medical_condition, activity_level)

    print("BMI:", round(bmi, 2))
    print("Recommendations:", recs)
    print("Notes:", notes)
