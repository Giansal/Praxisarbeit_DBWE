from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    print("SECRET_KEY:", app.config['SECRET_KEY'])
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"

    from . import routes, models, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(api.bp, url_prefix="/api")

    return app
