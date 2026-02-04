# Main Flask application
from flask import Flask, render_template, request
from src.recommendation import calculate_bmi, recommend_fitness

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = None
    notes = None
    bmi = None

    if request.method == "POST":
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        activity_level = request.form["activity_level"]
        medical_condition = request.form["medical_condition"]

        bmi = calculate_bmi(height, weight)
        recommendations, notes = recommend_fitness(
            age, bmi, medical_condition, activity_level
        )

    return render_template(
        "index.html",
        recommendations=recommendations,
        notes=notes,
        bmi=bmi
    )

if __name__ == "__main__":
    app.run(debug=True)
