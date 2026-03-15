from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.secret_key = "secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ======================
# DATABASE MODELS
# ======================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    email = db.Column(db.String(100))

    password = db.Column(db.String(100))


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    title = db.Column(db.String(200))

    description = db.Column(db.String(300))

    status = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ======================
# HOME
# ======================

@app.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return redirect("/login")


# ======================
# REGISTER
# ======================

@app.route("/register")
def register_page():

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    user = User(username=username, email=email, password=password)

    db.session.add(user)

    db.session.commit()

    return redirect("/login")


# ======================
# LOGIN
# ======================

@app.route("/login")
def login_page():

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email, password=password).first()

    if user:

        session["user_id"] = user.id

        return redirect("/dashboard")

    return "Invalid Login"


# ======================
# DASHBOARD
# ======================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    tasks = Task.query.filter_by(user_id=session["user_id"]).all()

    total = len(tasks)

    completed = len([t for t in tasks if t.status == "Completed"])

    pending = total - completed

    return render_template(
        "dashboard.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# ======================
# ADD TASK
# ======================

@app.route("/add_task", methods=["POST"])
def add_task():

    title = request.form["title"]

    description = request.form["description"]

    task = Task(
        user_id=session["user_id"],
        title=title,
        description=description,
        status="Pending"
    )

    db.session.add(task)

    db.session.commit()

    return redirect("/dashboard")


# ======================
# COMPLETE TASK
# ======================

@app.route("/complete/<int:id>")
def complete(id):

    task = Task.query.get(id)

    task.status = "Completed"

    db.session.commit()

    return redirect("/dashboard")


# ======================
# DELETE TASK
# ======================

@app.route("/delete/<int:id>")
def delete(id):

    task = Task.query.get(id)

    db.session.delete(task)

    db.session.commit()

    return redirect("/dashboard")


# ======================
# LOGOUT
# ======================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ======================
# RUN SERVER
# ======================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)