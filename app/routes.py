from flask import render_template

from app import app


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
