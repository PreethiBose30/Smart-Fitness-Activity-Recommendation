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
        activities = ["Meditation", "Breathing Exercises"]
    else:
        activities = ["HIIT", "Running"]

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
        user = request.form["username"]
        pwd = request.form["password"]
        goal = request.form["goal"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
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
        category = "Underweight" if bmi<18.5 else "Normal" if bmi<25 else "Overweight"
        calories=int(weight*30)

        activities,notes = smart_recommendation(
            bmi, mood, session["goal"], steps
        )

        today=str(datetime.date.today())

        conn=sqlite3.connect("users.db")
        c=conn.cursor()
        c.execute("INSERT INTO history VALUES (NULL,?,?,?,?,?,?)",
                  (session["user"],bmi,category,calories,today,steps))
        conn.commit()
        conn.close()

        return render_template("result.html",
                               bmi=bmi,
                               category=category,
                               calories=calories,
                               activities=activities,
                               notes=notes,
                               goal=session["goal"])

    return render_template("index.html", user=session["user"])

# ---------- HISTORY ----------
@app.route("/history")
def history():
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT bmi,category,calories,date,steps FROM history WHERE username=?",(session["user"],))
    data=c.fetchall()
    conn.close()

    return render_template("history.html", data=data)

# ---------- ANALYTICS ----------
@app.route("/analytics")
def analytics():
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT steps FROM history WHERE username=?",(session["user"],))
    steps=[x[0] for x in c.fetchall()]
    conn.close()

    avg = sum(steps)//len(steps) if steps else 0
    insight = "Great activity!" if avg>5000 else "Try to be more active"

    return render_template("analytics.html", avg=avg, insight=insight)

if __name__=="__main__":
    app.run(debug=True)
