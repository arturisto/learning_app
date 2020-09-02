import flask

user_blueprint = flask.Blueprint('users', __name__, template_folder="templates")

from . import views