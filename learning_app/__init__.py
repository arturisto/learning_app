import flask
import flask_sqlalchemy
import flask_migrate
import flask_mail
from flask_login import LoginManager
from .static import enums
import os

db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
login_manager = LoginManager()
mail_manager  = flask_mail.Mail()

def create_app(default_env = "production"):
    # imports
    from config import config
    from .views import main_blueprint
    from .user_managment import user_blueprint
    from .learning_hub import learning_hub_bp
    from . import models

    #learning_app init
    app = flask.Flask(__name__)

    # environment
    env = os.environ.get("FLASK_ENV", default_env)  # This will be different given the computer python is running on
    app.config.from_object(config[env])
    # learning_app.config['SECRET_KEY'] = "secretKey"
    # learning_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'learning_app.db')

    # components initializations
    db.init_app(app)
    mail_manager.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db)

    #blueprints:
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(learning_hub_bp, url_prefix="/hub")

    #constants:
    @app.context_processor
    def inject_constants():
        return {
            'UserRoles': enums.UserType
        }

    return app

