# Main Flask application
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    activities = []
    notes = []

    if request.method == "POST":
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        activity_level = request.form["activity"]
        medical = request.form["medical"]

        bmi = round(weight / (height * height), 2)

        # Simple recommendation logic
        if bmi < 18.5:
            activities = ["Walking", "Yoga", "Light strength training"]
            notes.append("Focus on healthy weight gain")
        elif 18.5 <= bmi < 25:
            activities = ["Jogging", "Cycling", "Strength training"]
            notes.append("Maintain current fitness level")
        else:
            activities = ["Walking", "Swimming", "Yoga"]
            notes.append("Avoid high-intensity workouts")

        if medical == "yes":
            notes.append("Consult a doctor before starting new exercises")

    return render_template(
        "index.html",
        bmi=bmi,
        activities=activities,
        notes=notes
    )

if __name__ == "__main__":
    app.run(debug=True)
