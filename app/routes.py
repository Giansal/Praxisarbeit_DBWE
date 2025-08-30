from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import db
from .models import User, Workout
from .forms import RegistrationForm, LoginForm, WorkoutForm

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registrierung erfolgreich! Bitte einloggen.")
        return redirect(url_for("routes.login"))
    return render_template("register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Login attempt: email={form.email.data}, password length={len(form.password.data)}")
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"User found: {user.email}")
        else:
            print("User not found")
        if user and user.check_password(form.password.data):
            print("Password correct, logging in")
            login_user(user)
            return redirect(url_for("routes.workouts"))
        else:
            print("Password incorrect or user not found")
        flash("Falsche Login-Daten")
    else:
        if form.errors:
            print("Form validation errors:", form.errors)
    return render_template("login.html", form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.index"))

@bp.route("/workouts", methods=["GET", "POST"])
@login_required
def workouts():
    form = WorkoutForm()
    if form.validate_on_submit():
        w = Workout(
            exercise=form.exercise.data,
            duration=form.duration.data,
            calories=form.calories.data,
            user_id=current_user.id
        )
        db.session.add(w)
        db.session.commit()
        flash("Workout gespeichert!")
        return redirect(url_for("routes.workouts"))

    workouts = Workout.query.filter_by(user_id=current_user.id).all()

    # Statistik berechnen
    total_workouts = len(workouts)
    total_duration = sum(w.duration for w in workouts)
    total_calories = sum(w.calories for w in workouts)
    average_duration = total_duration / total_workouts if total_workouts > 0 else 0

    return render_template(
        "workouts.html",
        form=form,
        workouts=workouts,
        total_workouts=total_workouts,
        total_duration=total_duration,
        total_calories=total_calories,
        average_duration=average_duration
    )

