from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    age = int(data["age"])
    height = float(data["height"])
    weight = float(data["weight"])

    # convert cm to meters if needed
    if height > 3:
        height = height / 100

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
        activities = ["Yoga", "Walking"]
    elif bmi < 25:
        category = "Normal"
        activities = ["Running", "Gym"]
    else:
        category = "Overweight"
        activities = ["Cardio", "Cycling"]

    return jsonify({
        "bmi": bmi,
        "category": category,
        "activities": activities
    })

if __name__ == "__main__":
    app.run(debug=True)
