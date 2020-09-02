import flask
from . import login_manager, mail_manager
from flask_mail import Message
from flask import request, flash, redirect, session, current_app
from learning_app.learning_hub import models as hub_models
from learning_app.user_managment import models as user_models
from .static import enums

main_blueprint = flask.Blueprint('main', __name__)


@main_blueprint.route('/', methods=['POST', 'GET'])
def index():
    """
    home page, shows the list of courses
    :return:
    """

    return flask.render_template('home.html')


@main_blueprint.route("/contact_form", methods=['POST', 'GET'])
def contact_form():
    """
    Sends an email to a predefined admin's email  with the contact
    """
    form = request.form
    # Create a mail
    msg = Message(
        subject=f"Website contact by {form['full_name']}",
        recipients=["arthurr.ie@gmail.com"],
        body=f" {form['full_name']} has filled a contact form on the front page\r\n"
             f"................ \r\n" \
             f"Contact Deatils:\r\n" \
             f"Email: {form['email']}\r\n" \
             f"Phone Number: {form['phone']}\r\n" \
             f"................\r\n" \
             f"Message:\r\n" \
             f"{form['text']}\r\n",
        sender=current_app.config["MAIL_USERNAME"]
    )

    # Send it !
    mail_manager.send(msg)

    flash("we have received, someone will contact you ASAP")
    return flask.render_template('home.html')


# # ----------------------start of error routes------------------------------------#
@main_blueprint.route('/getout')
@login_manager.unauthorized_handler
def unauthorized():
    return "This place is not for you, please leave"


# # ----------------------End of error routes------------------------------------#


@main_blueprint.route('/under_const')
def under_const():
    return flask.render_template("under_construction.html")