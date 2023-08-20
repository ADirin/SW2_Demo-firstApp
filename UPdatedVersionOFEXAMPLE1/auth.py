from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return '<p>Here comes the login page</p>'


@auth.route('/logout')
def logout():
    return '<p>Here comes the logout page</p>'
