import os
from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import (
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db, photos
from app.forms import LoginForm, ProfilePictureForm, RegistrationForm
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
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
    return render_template("index.html", title="Home", usr_tasks=usr_tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account has been registered")
        return redirect(url_for("login"))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    tasks = [
        {"asignee": user, "title": "Take out rubbish and recycling"},
        {
            "asignee": user,
            "title": "Clean room",
            "description": "Just yours",
            "helpers": "Miguel",
        },
    ]
    form = ProfilePictureForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        flash(f"Photo {filename} uploaded succesfully")
    return render_template("user.html", user=user, tasks=tasks, form=form)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        "".join(app.config["UPLOADED_PHOTOS_DEST"].split("/")[1:]), filename
    )
