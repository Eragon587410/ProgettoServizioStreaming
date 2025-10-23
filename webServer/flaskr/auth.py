from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)
from db import get_db, password_hash
from sqlalchemy import text

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=('GET', 'POST'))
def register():
    out = None
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        db.execute(text("INSERT INTO users (name, password) VALUES (:name, :password)"), {"name" : username, "password": password_hash(password)})
        db.commit()
        out = redirect(url_for('auth.login'))
        
    else:
        out = render_template('auth/register.html')
    return out

@bp.route('/login', methods=('GET', 'POST'))
def login():
    out = None
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        result = db.execute(text("SELECT * FROM users WHERE name = :username AND password = :password"), {"username" : username, "password" : password_hash(password)}).first()
        if result:
            out = redirect(url_for('films'))
            session['user'] = result[0]
        else:
            out = "credenziali errate"
    else:
        out = render_template('auth/login.html')
    return out

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


