from . import db, models, forms, login_manager
import sqlalchemy, flask_login



class CreateUser:
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def save_signup_data(self):             #Redundant - info in view file, either figure out how to call function in view or delete
        pass


