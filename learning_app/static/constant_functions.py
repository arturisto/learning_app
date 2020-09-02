from flask import session
from . import enums


def check_role(role):
    if session['role'] == role:
        return True
    else:
        return False
