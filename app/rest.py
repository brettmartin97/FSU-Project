from unicodedata import name
import pymysql
from app import app
from db import mysql
from flask import jsonify, Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import os
import hashlib
import utils.sql as sql
import logging
import utils.utils as utils

@app.route('/')
def home():
    session['auth'] = utils.is_auth(session)

    if not session['auth']:
        return redirect(url_for('login'))
    else:
        return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        
        valid = sql.validate_password(user, password, app.logger)

        if not valid:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['auth'] = True
            session['user'] = user
            session['level'] = sql.get_role(user)
            if session['level'] > 10:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    session['auth'] = utils.is_auth(session)
    if not session['auth']:
        return redirect(url_for('login'))
    else:
        firstname, lastname = sql.get_name(session['user'], app.logger)
        name = firstname + ' ' + lastname
        return render_template('admin.html', error=error, name=name)


if __name__ == "__main__":
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(debug=True,host='0.0.0.0')