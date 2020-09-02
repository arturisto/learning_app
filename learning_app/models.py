import datetime
import flask_sqlalchemy
import jwt
from flask_login import UserMixin
from flask_mail import Message
from . import db, login_manager, mail_manager
import flask
from flask import current_app