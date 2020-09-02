import flask

learning_hub_bp= flask.Blueprint('hub', __name__, template_folder="templates")

from . import management_views, main_views