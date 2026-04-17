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


def calculate_calories(weight):
    return int(weight * 30)


def get_diet_plan(category, food_type):

    if food_type == "veg":
        protein = "Paneer, Dal, Soy"
    else:
        protein = "Chicken, Eggs, Fish"

    if category == "Underweight":
        return ["Proteins", "Carbs", "Fats"], [40, 40, 20], {
            "Proteins": protein,
            "Carbs": "Rice, Bread, Fruits",
            "Fats": "Nuts, Butter"
        }

    elif category == "Normal":
        return ["Proteins", "Carbs", "Fats"], [30, 50, 20], {
            "Proteins": protein,
            "Carbs": "Rice, Chapati",
            "Fats": "Oil, Nuts"
        }

    else:
        return ["Proteins", "Carbs", "Fats"], [35, 40, 25], {
            "Proteins": protein,
            "Carbs": "Oats, Vegetables",
            "Fats": "Olive oil"
        }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            age = request.form["age"]
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            medical = request.form["medical_condition"]
            food_type = request.form["food_type"]

            if height > 3:
                height = height / 100

            bmi = round(weight / (height ** 2), 2)
            calories = calculate_calories(weight)

            activities, notes, category = get_recommendations(bmi, medical)

            return redirect(url_for("result",
                                    bmi=bmi,
                                    category=category,
                                    medical=medical,
                                    food_type=food_type,
                                    calories=calories))
        except:
            return "Invalid input! Please enter correct values."

    return render_template("index.html")


@app.route("/result")
def result():
    bmi = float(request.args.get("bmi"))
    category = request.args.get("category")
    medical = request.args.get("medical")
    food_type = request.args.get("food_type")
    calories = request.args.get("calories")

    activities, notes, category = get_recommendations(bmi, medical)

    return render_template("result.html",
                           bmi=bmi,
                           category=category,
                           activities=activities,
                           notes=notes,
                           food_type=food_type,
                           calories=calories)


@app.route("/diet")
def diet():
    bmi = request.args.get("bmi")
    category = request.args.get("category")
    food_type = request.args.get("food_type")

    labels, data, foods = get_diet_plan(category, food_type)

    return render_template("diet.html",
                           bmi=bmi,
                           category=category,
                           labels=labels,
                           data=data,
                           foods=foods,
                           food_type=food_type)


if __name__ == "__main__":
    app.run(debug=True)
