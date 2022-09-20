import pymysql
from app import app
from db import mysql
from flask import jsonify, Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import os
import hashlib
import utils.sql as sql
import logging

@app.route('/')
def home():
    try:
        if type(session['auth']) is bool:
            session['auth'] = session['auth']
        else:
            session['auth'] = False
    except:
        session['auth'] = False

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
        
        validationSQL = f'SELECT * FROM user WHERE username = "{user}" and password = "{password}"'

        conn = mysql.connect()

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute(validationSQL)

        valid = sql.validate_password(user, password, app.logger)

        if not valid:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['auth'] = True
            session['level'] = 5
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(debug=True,host='0.0.0.0')