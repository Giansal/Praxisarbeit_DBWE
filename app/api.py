from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Workout

bp = Blueprint("api", __name__)

@bp.route("/workouts")
@login_required
def get_workouts():
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            "date": w.date.isoformat(),
            "exercise": w.exercise,
            "duration": w.duration,
            "calories": w.calories
        }
        for w in workouts
    ])

