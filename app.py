from flask import Flask, render_template, request

app = Flask(__name__)

def get_recommendations(bmi, medical):
    activities = []
    notes = []

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
        notes.append("Avoid high intensity workouts")

    return activities, notes, category


def get_diet_plan(category, medical):
    if category == "Underweight":
        return {
            "labels": ["Proteins", "Carbs", "Fats"],
            "data": [40, 40, 20],
            "foods": {
                "Proteins": "Milk, Eggs, Paneer",
                "Carbs": "Rice, Bread, Fruits",
                "Fats": "Nuts, Butter"
            }
        }

    elif category == "Normal":
        return {
            "labels": ["Proteins", "Carbs", "Fats"],
            "data": [30, 50, 20],
            "foods": {
                "Proteins": "Chicken, Dal",
                "Carbs": "Rice, Chapati",
                "Fats": "Oil, Nuts"
            }
        }

    else:  # Overweight
        return {
            "labels": ["Proteins", "Carbs", "Fats"],
            "data": [35, 40, 25],
            "foods": {
                "Proteins": "Lean meat, Lentils",
                "Carbs": "Oats, Vegetables",
                "Fats": "Olive oil"
            }
        }


@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = None
    recommendations = []
    notes = []

    age = ""
    height = ""
    weight = ""
    activity = ""
    medical = ""

    if request.method == "POST":
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        activity = request.form["activity_level"]
        medical = request.form["medical_condition"]

        try:
            height = float(height)
            weight = float(weight)

            if height > 3:
                height = height / 100

            bmi = round(weight / (height ** 2), 2)

            recommendations, notes, category = get_recommendations(bmi, medical)

        except:
            bmi = None

    return render_template("index.html",
                           bmi=bmi,
                           category=category,
                           recommendations=recommendations,
                           notes=notes,
                           age=age,
                           height=height,
                           weight=weight,
                           activity=activity,
                           medical=medical)


@app.route("/diet")
def diet():
    category = request.args.get("category")
    medical = request.args.get("medical")

    diet_plan = get_diet_plan(category, medical)

    return render_template("diet.html",
                           labels=diet_plan["labels"],
                           data=diet_plan["data"],
                           foods=diet_plan["foods"],
                           category=category)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
