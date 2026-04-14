from flask import Flask, render_template, request

app = Flask(__name__)

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

    return render_template("index.html", recommendation=recommendation)


if __name__ == '__main__':
    app.run(debug=True)
