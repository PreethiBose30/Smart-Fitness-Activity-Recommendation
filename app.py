from flask import Flask, render_template, request

app = Flask(__name__)

<<<<<<< HEAD
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendation = None

    if request.method == 'POST':
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        goal = request.form['goal']
        diet = request.form['diet']

        # Simple logic
        if goal == "weight_loss":
            activity = "Cardio and HIIT workouts"
        elif goal == "muscle_gain":
            activity = "Strength training and weight lifting"
        else:
            activity = "Balanced workout routine"

        if diet == "veg":
            diet_plan = "High-protein vegetarian diet with paneer, lentils, tofu."
        else:
            diet_plan = "High-protein non-veg diet with chicken, eggs, fish."

        recommendation = f"""
        Age: {age}
        Suggested Activity: {activity}
        Suggested Diet: {diet_plan}
        """
=======
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

        bmi = round(float(weight) / (float(height) ** 2), 2)

        recommendations, notes, category = get_recommendations(bmi, medical)

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
    return render_template("diet.html")


@app.route("/about")
def about():
    return render_template("about.html")

>>>>>>> 1e3b0c3f62db37affb0544fb8c85f6f2f7923b3f

    return render_template("index.html", recommendation=recommendation)


if __name__ == '__main__':
    app.run(debug=True)
