from flask import Flask, render_template, request, redirect, url_for

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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        medical = request.form["medical_condition"]

        height = float(height)
        weight = float(weight)

        if height > 3:
            height = height / 100

        bmi = round(weight / (height ** 2), 2)

        activities, notes, category = get_recommendations(bmi, medical)

        return redirect(url_for("result",
                                bmi=bmi,
                                category=category,
                                medical=medical))

    return render_template("index.html")


@app.route("/result")
def result():
    bmi = request.args.get("bmi")
    category = request.args.get("category")
    medical = request.args.get("medical")

    bmi = float(bmi)

    activities, notes, category = get_recommendations(bmi, medical)

    return render_template("result.html",
                           bmi=bmi,
                           category=category,
                           activities=activities,
                           notes=notes,
                           medical=medical)


@app.route("/diet")
def diet():
    bmi = request.args.get("bmi")
    category = request.args.get("category")

    labels, data, foods = get_diet_plan(category)

    return render_template("diet.html",
                           bmi=bmi,
                           category=category,
                           labels=labels,
                           data=data,
                           foods=foods)


if __name__ == "__main__":
    app.run(debug=True)
