from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField("Benutzername", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("E-Mail", validators=[DataRequired(), Email()])
    password = PasswordField("Passwort", validators=[DataRequired()])
    password2 = PasswordField("Passwort wiederholen", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrieren")

class LoginForm(FlaskForm):
    email = StringField("E-Mail", validators=[DataRequired(), Email()])
    password = PasswordField("Passwort", validators=[DataRequired()])
    submit = SubmitField("Einloggen")

class WorkoutForm(FlaskForm):
    exercise = StringField("Übung", validators=[DataRequired()])
    duration = IntegerField("Dauer (Minuten)", validators=[DataRequired()])
    calories = IntegerField("Kalorien")
    submit = SubmitField("Speichern")
