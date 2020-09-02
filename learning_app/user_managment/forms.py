import flask_wtf
import wtforms as wtf
from wtforms import validators as valid
from wtforms.fields.html5 import EmailField
from ..static.enums import UserType
from .. import db
from . import models


class CreateUser(flask_wtf.FlaskForm):
    """
    Form for creat user page

    """
    name = wtf.StringField('Name', [valid.InputRequired(message="Name required for signup")])
    username = wtf.StringField('User Name', [valid.InputRequired(message="Username required for signup")])
    email = EmailField('Email', [valid.Email(message="Must enter valid email address")])
    password = wtf.PasswordField("Password", [valid.InputRequired(message="Must enter a password")])
    confirm_pass = wtf.PasswordField("Confirm Password", [valid.EqualTo(password, message="Passwords must match")])
    role = wtf.SelectField("Role", choices=[(type.name, type.value) for type in UserType])
    submit = wtf.SubmitField('Sign Up')


class Login(flask_wtf.FlaskForm):
    """
    Form for login page
    """
    email = wtf.StringField('Email', [valid.Email(message='Must enter account email')])
    password = wtf.PasswordField('Password', [valid.InputRequired(message='Please enter password')])
    submit = wtf.SubmitField('Login')


class password_reset(flask_wtf.FlaskForm):
    """
    Form for password Reset
    """
    email = wtf.HiddenField("user_email")
    password = wtf.PasswordField("Password", [valid.InputRequired(message="Must enter a password")],
                                 render_kw={"class": "form-control"})
    confirm_pass = wtf.PasswordField("Confirm Password",
                                     [valid.EqualTo(password, message="Passwords must match")],
                                     render_kw={"class": "form-control"}
                                     )

    submit = wtf.SubmitField('Enroll Me', render_kw={"class": "btn btn-primary"})




