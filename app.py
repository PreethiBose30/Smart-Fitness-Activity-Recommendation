from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        bmi REAL,
        category TEXT,
        calories INTEGER
    )''')

    conn.commit()
    conn.close()

init_db()

# ---------- LOGIC ----------
def get_recommendations(bmi, medical):
    activities = []
    notes = []

    if bmi < 18.5:
        activities = ["Walking", "Yoga", "Light strength training"]
        category = "Underweight"
    elif bmi < 25:
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
    protein = "Paneer, Dal, Soy" if food_type == "veg" else "Chicken, Eggs, Fish"

    return ["Proteins", "Carbs", "Fats"], [30, 50, 20], {
        "Proteins": protein,
        "Carbs": "Rice, Chapati",
        "Fats": "Nuts, Oil"
    }

# ---------- AUTH ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (user, pwd))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------- MAIN ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        medical = request.form["medical_condition"]
        food_type = request.form["food_type"]

        if height > 3:
            height /= 100

        bmi = round(weight / (height ** 2), 2)
        calories = calculate_calories(weight)

        activities, notes, category = get_recommendations(bmi, medical)

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO history (username, bmi, category, calories) VALUES (?, ?, ?, ?)",
            (session["user"], bmi, category, calories)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("result",
                                bmi=bmi,
                                category=category,
                                medical=medical,
                                food_type=food_type,
                                calories=calories))

    return render_template("index.html", user=session["user"])


@app.route("/result")
def result():
    bmi = request.args.get("bmi")
    medical = request.args.get("medical")

    activities, notes, _ = get_recommendations(float(bmi), medical)

    return render_template("result.html",
                           bmi=bmi,
                           category=request.args.get("category"),
                           food_type=request.args.get("food_type"),
                           calories=request.args.get("calories"),
                           activities=activities,
                           notes=notes)


@app.route("/diet")
def diet():
    labels, data, foods = get_diet_plan(
        request.args.get("category"),
        request.args.get("food_type")
    )

    return render_template("diet.html",
                           bmi=request.args.get("bmi"),
                           category=request.args.get("category"),
                           labels=labels,
                           data=data,
                           foods=foods,
                           food_type=request.args.get("food_type"))


@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT bmi, category, calories FROM history WHERE username=?", (session["user"],))
    data = c.fetchall()
    conn.close()

    return render_template("history.html", data=data)
    

if __name__ == "__main__":
    app.run(debug=True)
