from flask import Flask, render_template, request

app = Flask(__name__)

def get_recommendations(bmi, medical):
    activities = []
    notes = []

    if bmi < 18.5:
        activities = ["Walking", "Yoga", "Light strength training"]
        notes.append("Focus on healthy weight gain")
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        activities = ["Jogging", "Cycling", "Strength training"]
        notes.append("Maintain balanced lifestyle")
        category = "Normal"
    else:
        activities = ["Cardio", "Swimming", "Brisk walking"]
        notes.append("Focus on weight reduction")
        category = "Overweight"

    if medical == "yes":
        notes.append("Avoid high intensity workouts")

    return activities, notes, category


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

            # convert cm to meters automatically
            if height > 3:
                height = height / 100

            bmi = round(weight / (height ** 2), 2)

            recommendations, notes, category = get_recommendations(bmi, medical)

        except:
            bmi = None

    return render_template(
        "index.html",
        bmi=bmi,
        category=category,
        recommendations=recommendations,
        notes=notes,
        age=age,
        height=height,
        weight=weight,
        activity=activity,
        medical=medical
    )


@app.route("/diet")
def diet():
    return render_template("diet.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
