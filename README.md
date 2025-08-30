# Fitness Tracker App

## Übersicht
Webanwendung zur Registrierung und Verwaltung von Workouts.

## Installation

```bash
git clone https://github.com/Giansal/Praxisarbeit_DBWE.git
cd Praxisarbeit_DBWE
cp .env.example .env
# .env mit realen Werten füllen
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
