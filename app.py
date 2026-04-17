from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_recommendations(bmi, medical):
    if bmi < 18.5:
        activities = ["Walking", "Yoga", "Light strength training"]
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        activities = ["Jogging", "Cycling", "Strength training"]
        category = "Normal"
    else:
        activities = ["Cardio", "Swimming", "Brisk walking"]
        category = "Overweight"

    if medical == "yes":
        activities.append("Consult doctor before workouts")

    return activities, category


def get_diet_plan(category):
    if category == "Underweight":
        return ["Proteins", "Carbs", "Fats"], [40, 40, 20], {
            "Proteins": "Milk, Eggs, Paneer",
            "Carbs": "Rice, Bread",
            "Fats": "Nuts, Butter"
        }
    elif category == "Normal":
        return ["Proteins", "Carbs", "Fats"], [30, 50, 20], {
            "Proteins": "Chicken, Dal",
            "Carbs": "Rice, Chapati",
            "Fats": "Oil, Nuts"
        }
    else:
        return ["Proteins", "Carbs", "Fats"], [35, 40, 25], {
            "Proteins": "Lean meat, Lentils",
            "Carbs": "Oats, Veggies",
            "Fats": "Olive oil"
        }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    age = int(data["age"])
    height = float(data["height"])
    weight = float(data["weight"])
    goal = data["goal"]
    medical = data["medical"]

    # convert cm → meters if needed
    if height > 3:
        height = height / 100

    bmi = round(weight / (height ** 2), 2)

    activities, category = get_recommendations(bmi, medical)
    labels, chart_data, foods = get_diet_plan(category)

    calories = int(10 * weight + 6.25 * (height * 100) - 5 * age)
    water = round(weight * 0.033, 2)
    workout = "30–45 mins" if category == "Normal" else "45–60 mins"

    return jsonify({
        "bmi": bmi,
        "category": category,
        "activities": activities,
        "labels": labels,
        "chart_data": chart_data,
        "foods": foods,
        "calories": calories,
        "water": water,
        "workout": workout
    })


if __name__ == "__main__":
    app.run(debug=True)
