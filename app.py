from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, datetime

app = Flask(__name__)
app.secret_key = "secret"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        goal TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        username TEXT,
        bmi REAL,
        category TEXT,
        calories INTEGER,
        date TEXT,
        steps INTEGER
    )''')

    conn.commit()
    conn.close()

init_db()

# ---------- SMART ENGINE ----------
def smart_recommendation(bmi, mood, goal, steps):
    activities = []
    notes = []

    if mood == "tired":
        activities = ["Light Yoga", "Stretching"]
    elif mood == "stressed":
        activities = ["Meditation", "Breathing"]
    else:
        activities = ["Running", "HIIT"]

    if steps < 3000:
        notes.append("You are less active today. Try walking more.")

    if goal == "weight_loss":
        activities.append("Cardio")
    elif goal == "muscle":
        activities.append("Strength Training")

    return activities, notes

# ---------- AUTH ----------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        user=request.form["username"]
        pwd=request.form["password"]
        goal=request.form["goal"]

        conn=sqlite3.connect("users.db")
        c=conn.cursor()
        c.execute("INSERT INTO users VALUES (NULL,?,?,?)",(user,pwd,goal))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=request.form["username"]
        pwd=request.form["password"]

        conn=sqlite3.connect("users.db")
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",(user,pwd))
        result=c.fetchone()
        conn.close()

        if result:
            session["user"]=user
            session["goal"]=result[3]
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- HOME ----------
@app.route("/", methods=["GET","POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    if request.method=="POST":
        height=float(request.form["height"])
        weight=float(request.form["weight"])
        mood=request.form["mood"]
        steps=int(request.form["steps"])

        if height>3:
            height/=100

        bmi=round(weight/(height**2),2)

        if bmi < 18.5:
            category="Underweight"
        elif bmi < 25:
            category="Normal"
        else:
            category="Overweight"

        calories=int(weight*30)

        activities,notes=smart_recommendation(bmi,mood,session["goal"],steps)

        today=str(datetime.date.today())

        conn=sqlite3.connect("users.db")
        c=conn.cursor()
        c.execute("INSERT INTO history VALUES (NULL,?,?,?,?,?,?)",
                  (session["user"],bmi,category,calories,today,steps))
        conn.commit()
        conn.close()

        return redirect(url_for("result",
                               bmi=bmi,
                               category=category,
                               calories=calories))

    return render_template("index.html", user=session["user"])

# ---------- RESULT ----------
@app.route("/result")
def result():
    bmi=float(request.args.get("bmi"))
    category=request.args.get("category")
    calories=request.args.get("calories")

    activities,notes=smart_recommendation(bmi,"energetic",session["goal"],5000)

    return render_template("result.html",
                           bmi=bmi,
                           category=category,
                           calories=calories,
                           activities=activities,
                           notes=notes)

# ---------- SMART DIET ----------
@app.route("/diet")
def diet():
    category = request.args.get("category")
    bmi = float(request.args.get("bmi", 0))
    goal = session.get("goal", "fitness")

    # CALORIES BASED ON GOAL
    if goal == "weight_loss":
        calories = 1800
    elif goal == "muscle":
        calories = 2500
    else:
        calories = 2200

    # DIET LOGIC
    if category == "Underweight":
        labels = ["Proteins", "Carbs", "Fats"]
        data = [25, 55, 20]
        meals = {
            "Breakfast": "Milk, Banana, Peanut Butter",
            "Lunch": "Rice, Dal, Paneer",
            "Dinner": "Chapati, Vegetables",
            "Snacks": "Nuts, Smoothie"
        }

    elif category == "Normal":
        labels = ["Proteins", "Carbs", "Fats"]
        data = [30, 50, 20]
        meals = {
            "Breakfast": "Eggs / Oats",
            "Lunch": "Rice, Chicken/Dal",
            "Dinner": "Chapati, Veg",
            "Snacks": "Fruits, Nuts"
        }

    else:
        labels = ["Proteins", "Carbs", "Fats"]
        data = [35, 40, 25]
        meals = {
            "Breakfast": "Oats, Fruits",
            "Lunch": "Grilled chicken / Dal",
            "Dinner": "Salad, Soup",
            "Snacks": "Green tea, Nuts"
        }

    return render_template("diet.html",
                           category=category,
                           bmi=bmi,
                           calories=calories,
                           labels=labels,
                           data=data,
                           meals=meals,
                           goal=goal)

@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT steps, date FROM history WHERE username=?", (session["user"],))
    data = c.fetchall()
    conn.close()

    if not data:
        return render_template("analytics.html",
                               avg=0,
                               insight="No data yet",
                               steps=[],
                               dates=[],
                               best_day="N/A",
                               score=0,
                               improvement=0)

    steps = [row[0] for row in data]
    dates = [row[1] for row in data]

    # ---------- AVERAGE ----------
    avg = sum(steps) // len(steps)

    # ---------- ACTIVITY SCORE ----------
    score = min(100, int(avg / 100))   # simple score logic

    # ---------- BEST DAY ----------
    max_steps = max(steps)
    best_day = dates[steps.index(max_steps)]

    # ---------- IMPROVEMENT ----------
    if len(steps) > 1:
        improvement = steps[-1] - steps[0]
    else:
        improvement = 0

    # ---------- INSIGHTS ----------
    if avg > 8000:
        insight = "🔥 Excellent consistency!"
    elif avg > 5000:
        insight = "👍 Good progress, keep pushing!"
    else:
        insight = "⚠️ You need to be more active."

    return render_template("analytics.html",
                           avg=avg,
                           insight=insight,
                           steps=steps,
                           dates=dates,
                           best_day=best_day,
                           score=score,
                           improvement=improvement)
    
# ---------- RUN ----------
if __name__=="__main__":
    app.run(debug=True)
