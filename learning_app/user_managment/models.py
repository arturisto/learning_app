import datetime
import flask_sqlalchemy
import jwt
from flask_login import UserMixin
from flask_mail import Message
from .. import db, login_manager, mail_manager
import flask
from flask import current_app




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(264))
    username = db.Column(db.String(264), unique=True)
    email = db.Column(db.String(264), unique=True)
    password = db.Column(db.String(264))
    role = db.Column(db.PickleType())
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    class_name = db.relationship("Class", back_populates="users")

    def send_pass_link(self):
        payload = {
            'user_id': self.id,
            'expires': (datetime.datetime.now() + datetime.timedelta(hours=2)).timestamp()
        }

        token = jwt.encode(payload, current_app.config["SECRET_KEY"])

        url = flask.url_for('users.reset_password', jwt_token=token, _external=True)
        # Create a mail
        msg = Message(
            subject="Password Reset",
            recipients=[self.email],
            body=f"Hello {self.name}, to reset your password, navigate to {url}",
            sender=current_app.config["MAIL_USERNAME"]
        )

        # Send it !
        mail_manager.send(msg)


class Class(db.Model, UserMixin):
    __tablename__="class"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(264))
    max_capacity = db.Column(db.Integer)
    users = db.relationship("User", back_populates="class_name")



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
