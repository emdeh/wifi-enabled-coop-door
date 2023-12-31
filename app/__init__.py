from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig
from .models import User
from .hardware_control import setup_hardware  # Assuming you have a setup_hardware function
import time
from threading import Thread

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Define your routes here
    from .routes import configure_routes
    configure_routes(app)

    # Setup hardware and scheduled tasks
    if setup_hardware(app):
        from .scheduled_tasks import start_scheduler
        start_scheduler()  # Assuming you have a function to start the scheduler

    return app
