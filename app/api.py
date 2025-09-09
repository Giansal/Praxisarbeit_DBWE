from flask import Blueprint, request, jsonify
from .models import User, Workout
from . import db
import secrets

bp = Blueprint("api", __name__)

# Einfacher Token-Speicher im Speicher (nicht persistent!)
tokens = {}


@bp.route("/login", methods=["POST"])
def api_login():
    """API-Login: Benutzer meldet sich mit Email + Passwort an
       und erhält einen Token zurück."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = secrets.token_hex(16)
        tokens[token] = user.id
        print(f"[DEBUG] Neuer Token erstellt: {token} für User-ID {user.id}")
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/workouts", methods=["GET"])
def api_workouts():
    """API-Endpunkt: Liste aller Workouts des eingeloggten Benutzers."""
    auth_header = request.headers.get("Authorization")
    print("[DEBUG] Authorization Header:", auth_header)

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.replace("Bearer ", "")
    print("[DEBUG] Extrahierter Token:", token)

    user_id = tokens.get(token)
    print("[DEBUG] Gefundene User-ID:", user_id)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    workouts = Workout.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": w.id,
            "exercise": w.exercise,
            "duration": w.duration,
            "calories": w.calories,
            "date": w.date.strftime("%Y-%m-%d")
        }
        for w in workouts
    ])
