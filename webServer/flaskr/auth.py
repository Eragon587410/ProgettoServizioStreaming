from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as br_session, url_for,
)
import db.models as models
from sqlalchemy import text
import hashlib

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=('GET', 'POST'))
def register():
    out = None
    if request.method == 'POST':
        #db = get_db()
        username = request.form['username']
        password = request.form['password']
        #db.execute(text("INSERT INTO users (name, password) VALUES (:name, :password)"), {"name" : username, "password": password_hash(password)})
        #db.commit()
        with models.User.session() as session:
            user = models.User(session=session, username=username)
            if user.persistent:
                out = "username già in uso"
            else:
                user.set_password(password)
                session.add(user)
                session.commit()
                out = redirect(url_for('auth.login'))
        
    else:
        out = render_template('auth/register.html')
    return out

@bp.route('/login', methods=('GET', 'POST'))
def login():
    out = None
    if request.method == 'POST':
        #db = get_db()
        username = request.form['username']
        password = request.form['password']
        #result = db.execute(text("SELECT * FROM users WHERE name = :username AND password = :password"), {"username" : username, "password" : password_hash(password)}).first()
        with models.User.session() as session:
            record = models.User(session=session, username=username)
            if record.persistent and record.login(password):
                out = redirect(url_for('films'))
                br_session['user'] = record.username
            else:
                out = "credenziali errate"
    else:
        out = render_template('auth/login.html')
    return out

@bp.route('/logout')
def logout():
    br_session.clear()
    return redirect(url_for('auth.login'))


