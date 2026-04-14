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

    notes = []
    if medical == "yes":
        notes.append("Avoid high intensity workouts")

    return activities, notes, category


def get_diet_plan(category):
    if category == "Underweight":
        return ["Proteins", "Carbs", "Fats"], [40, 40, 20], {
            "Proteins": "Milk, Eggs, Paneer",
            "Carbs": "Rice, Bread, Fruits",
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
            "Carbs": "Oats, Vegetables",
            "Fats": "Olive oil"
        }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    height = float(data["height"])
    weight = float(data["weight"])
    medical = data["medical"]

    if height > 3:
        height = height / 100

    bmi = round(weight / (height ** 2), 2)

    activities, notes, category = get_recommendations(bmi, medical)
    labels, chart_data, foods = get_diet_plan(category)

    return jsonify({
        "bmi": bmi,
        "category": category,
        "activities": activities,
        "notes": notes,
        "labels": labels,
        "chart_data": chart_data,
        "foods": foods
    })


if __name__ == "__main__":
    app.run(debug=True)
