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
import yaml

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
            where = f'username = "{user}"'
            session['level'] = sql.get_attribute("roleId", "User", where)
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
        if request.method == 'POST':
            userId = request.form['userId']
            return redirect(url_for('edit_user',  userId=userId))
        else:
            users = sql.get_table('User')
            roles = sql.get_table('Role')
            return render_template('user_management.html', error=error, users=users, roles=roles)

@app.route('/admin/user_management/<userId>', methods=['GET', 'POST'])
def edit_user(userId):
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            user = sql.get_user(userId)
            app.logger.info(user)
            if request.form['firstName'] != user['firstName'] :
                sql.update_user(userId,f"firstName = '{request.form['firstName']}'")
            if request.form['lastName'] != user['lastName']:
                sql.update_user(userId,f"lastName = '{request.form['lastName']}'")
            if request.form['phone'] != user['phone']:
                sql.update_user(userId,f"phone = {request.form['phone']}")
            if request.form['email'] != user['email'] :
                sql.update_user(userId,f"email = '{request.form['email']}'")
            if request.form['roleId'] != user['roleId']:
                app.logger.info(f"roleId = {request.form['roleId']}")
                sql.update_user(userId,f"roleId = {request.form['roleId']}")
            return redirect(url_for('edit_user', userId=user['userId']))
        else:
            user = sql.get_user(userId)
            with open("config/config.yml") as f:
                config = yaml.safe_load(f)
            maxRole = config['site']['maxRole']
            return render_template('edit_user.html', error=error, user=user, maxRole=maxRole)

@app.route('/admin/site_management', methods=['GET', 'POST'])
def site_management():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            with open("config/config.yml") as f:
                config = yaml.safe_load(f)
            maxRole = request.form['maxRole']
            startTime = request.form['open']
            endTime = request.form['close']
            config['site']['maxRole'] = maxRole
            config['site']['open'] = startTime
            config['site']['close'] = endTime
            with open("config/config.yml", "w") as f:
                yaml.dump(config, f)
        else:
            with open("config/config.yml") as f:
                config = yaml.safe_load(f)
            app.logger.info(config)
            maxRole = config['site']['maxRole']
            startTime = config['site']['open']
            endTime = config['site']['close']
        return render_template('site_management.html', error=error, maxRole=maxRole, startTime=startTime, endTime=endTime)

@app.route('/admin/user_management/add_user', methods=['GET', 'POST'])
def add_user():
    error = None
    auth_bool = utils.is_auth(session)
    if request.method == 'POST':
        firstName = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['email']
        un = request.form['username']
        pwd = request.form['password']
        phone = request.form['phone']
        role = request.form['role']
        booth = request.form['booth']
        sql.insert_User(firstName, lname, email, phone, un, pwd, role, 0)
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
        customers = sql.get_table('Customer')
        return render_template('customers.html', error=error, customers = customers)

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

@app.route('/admin/calendar/<day>.<month>.<year>', methods   =['GET', 'POST'])
def calendarDay(day,month,year):
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        times = []
        date = datetime(int(year),int(month),int(day),9,0,0)
        formateddate = date.strftime("%I:%M %p")
        times.append(formateddate)
        weekday = date.weekday()
        user_schedule = sql.get_schedule(weekday)
        
        for i in range(40): 
            date += timedelta(minutes=15)
            formateddate = date.strftime("%I:%M %p")
            times.append(formateddate)
        
        return render_template('Calendar-Day.html', day=day, month=month, year=year, times=times,user_schedule=user_schedule, datetime=datetime)

@app.route('/admin/calendar', methods=['GET', 'POST'])
def calendarmonth():
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
                day = int(request.form['submit_button'])
                month = request.form['month']
                intmonth = datetime.strptime(month, "%B")
                month = int(intmonth.month)
                year = int(request.form['year'])
                return redirect(url_for('calendarDay', day=day, month=month, year=year))
        elif request.method == 'GET':
            date = datetime.now()
        currentDay = date.day
        currentMonth = date.strftime("%B")
        currentYear = date.year
        firstDay = date.replace(day=1).weekday()
        lastDay = date.replace(day = calendar.monthrange(date.year, date.month)[1]).strftime("%d")
        return render_template('Calendar-Month.html', lastDay = int(lastDay), 
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
        aptChart = sql.appointment_chart()
        styChart = sql.by_user_chart()
        return render_template('analysis.html', error=error, aptChart=aptChart, styChart = styChart)


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