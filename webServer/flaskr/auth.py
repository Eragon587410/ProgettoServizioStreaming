from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)
from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=('GET', 'POST'))
def register():
    out = None
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        
    else:
        out = render_template('auth/register.html')
    return out

@bp.route('/login', methods=('GET', 'POST'))
def login():
    out = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        out = f"{username} + {password}"
    else:
        out = render_template('auth/login.html')
    return out