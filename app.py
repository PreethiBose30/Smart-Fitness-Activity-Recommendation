from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    height = float(data["height"])
    weight = float(data["weight"])
    diet = data["diet"]

    if height > 3:
        height = height / 100

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    else:
        category = "Overweight"

    # 🍽️ DIET LOGIC
    if diet == "veg":
        foods = {
            "Breakfast": "Oats, Fruits, Milk",
            "Lunch": "Rice, Dal, Vegetables",
            "Dinner": "Chapati, Paneer"
        }
    else:
        foods = {
            "Breakfast": "Eggs, Milk, Bread",
            "Lunch": "Chicken, Rice",
            "Dinner": "Fish, Vegetables"
        }

    return jsonify({
        "bmi": bmi,
        "category": category,
        "foods": foods
    })

if __name__ == "__main__":
    app.run(debug=True)
