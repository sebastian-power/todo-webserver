from flask import flash, redirect, render_template, url_for

from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Miguel"}
    usr_tasks = [
        {
            "task_title": "Clean bathroom",
            "task_desc": "One person do mirrors and bench and the other does toilet and bath",
            "due_date": "25/01/2024(3 days)",
            "helpers": "Gustavo",
        },
        {
            "task_title": "Clean windows",
            "due_date": "27/01/2024 - 29/01/2024",
        },
    ]
    return render_template("index.html", title="Home", user=user, usr_tasks=usr_tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)
