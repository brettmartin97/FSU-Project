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
import calendar
from datetime import datetime, timedelta

@app.route('/')
def home():
    auth_bool = utils.is_auth(session)

    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

@app.route('/booth')
def booth():
    auth_bool = utils.is_auth(session)
    if not auth_bool: 
        return redirect(url_for('login'))
    elif session['level'] != 11:
        return redirect(url_for('error'))
    else:
        return render_template('booth.html')


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
            session['level'] = sql.get_attribute(user, "role", "User")
            if session['level'] > 11:
                return redirect(url_for('admin'))
            elif session['level'] == 11:
                return redirect(url_for('booth'))
            else:
                return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        firstname, lastname = sql.get_name(session['user'], app.logger)
        name = firstname + ' ' + lastname
        return render_template('admin.html', error=error, name=name, title='admin')


@app.route('/admin/user_management', methods=['GET', 'POST'])
def user_management():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('user_management.html', error=error)

@app.route('/admin/user_management/add_user', methods=['GET', 'POST'])
def add_user():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('add_user.html', error=error)

@app.route('/admin/customer_management', methods=['GET', 'POST'])
def customers():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('customers.html', error=error)

@app.route('/admin/appointments', methods=['GET', 'POST'])
def appointments():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        appointments = sql.get_table('AppointmentType')
        return render_template('appointments.html', error=error, appointments = appointments)

@app.route('/admin/appointments/add_appointment')
def add_appointment():
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('add_appointment.html', error=error)

@app.route('/admin/booking/<day>.<month>.<year>', methods   =['GET', 'POST'])
def bookingDay(day,month,year):
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('booking_day.html', date=date)

@app.route('/admin/booking', methods=['GET', 'POST'])
def booking():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Next Month':
                date = request.form['date']
                date = datetime.strptime(date, '%Y-%m-%d')
                last = date.replace(day = calendar.monthrange(date.year, date.month)[1])
                date = last + timedelta(days=1)
            elif request.form['submit_button'] == 'Prev Month':
                date = request.form['date']
                date = datetime.strptime(date, '%Y-%m-%d')
                first = date.replace(day=1)
                date = first - timedelta(days=1)
            else:
                date = request.form['submit_button']
                return redirect(url_for('bookingDay', date=date))
        elif request.method == 'GET':
            date = datetime.now()
        currentDay = date.day
        currentMonth = date.strftime("%B")
        currentYear = date.year
        firstDay = date.replace(day=1).weekday()
        lastDay = date.replace(day = calendar.monthrange(date.year, date.month)[1]).strftime("%d")
        return render_template('booking.html', lastDay = int(lastDay), 
        firstDay=firstDay, day=currentDay, month=currentMonth, 
        year=currentYear, date=date, error=error)

@app.route('/admin/analysis', methods=['GET', 'POST'])
def analysis():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        firstname, lastname = sql.get_name(session['user'], app.logger)
        name = firstname + ' ' + lastname
        return render_template('analysis.html', error=error)

@app.route('/admin/scheduling/<date>', methods=['GET', 'POST'])
def scheduleDay(date):
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('schedule_day.html', date=date)

@app.route('/admin/scheduling', methods=['GET', 'POST'])
def scheduling():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Next Month':
                date = request.form['date']
                date = datetime.strptime(date, '%Y-%m-%d')
                last = date.replace(day = calendar.monthrange(date.year, date.month)[1])
                date = last + timedelta(days=1)
            elif request.form['submit_button'] == 'Prev Month':
                date = request.form['date']
                date = datetime.strptime(date, '%Y-%m-%d')
                first = date.replace(day=1)
                date = first - timedelta(days=1)
            else:
                date = request.form['submit_button']
                return redirect(url_for('scheduleDay', date=date))
        elif request.method == 'GET':
            date = datetime.now()
        currentDay = date.day
        currentMonth = date.strftime("%B")
        currentYear = date.year
        firstDay = date.replace(day=1).weekday()
        lastDay = date.replace(day = calendar.monthrange(date.year, date.month)[1]).strftime("%d")
        return render_template('scheduling.html', lastDay = int(lastDay), 
        firstDay=firstDay, day=currentDay, month=currentMonth, 
        year=currentYear, date=date, error=error)


@app.route('/logout', methods=['GET'])
def logout():
    session['auth'] = None
    session['user'] = None
    session['level'] = None
    return redirect(url_for('login'))

@app.route('/error')
def error():
    return render_template('404.html', title='error page not found')

if __name__ == "__main__":
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(debug=True,host='0.0.0.0')