from unicodedata import name
import pymysql
from app import app
from db import mysql
from flask import jsonify, Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import os
import utils.hashing as hashing
import utils.sql as sql
import logging
import utils.utils as utils
import calendar as fcalendar
from datetime import datetime, timedelta
import yaml
import re

@app.route('/')
def home():
    auth_bool = utils.is_auth(session)

    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

@app.route('/booth', methods=['GET', 'POST'])
def booth():
    auth_bool = utils.is_auth(session)
    if not auth_bool: 
        return redirect(url_for('login'))
    elif session['level'] != 11:
        return redirect(url_for('error'))
    else:
        return render_template('booth.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    error=None
    if len(sql.get_table("User")) > 0:
        return redirect(url_for('login'))

    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    where = f'username = "{user}"'
    session['level'] = sql.get_attribute_single("roleId", "User", where)
    len(get_table("User"))
    return render_template('setup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        
        valid = sql.validate_password(user, password)

        if not valid:
            error = 'Invalid Credentials. Please try again.'
        else:
            if len(sql.get_table("User")) == 0:
                return redirect(url_for('setup'))
            session['auth'] = True
            session['user'] = user
            where = f'username = "{user}"'
            app.logger.info(sql.get_attribute_single("roleId", "User", where))
            session['admin'] = sql.get_attribute_single("management", "User", where)
            if session['admin']:
                return redirect(url_for('admin'))
            elif session['admin']:
                return redirect(url_for('booth'))
            else:
                return redirect(url_for('home'))
    return render_template('login.html', error=error, company=company)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        firstname, lastname = sql.get_name(session['user'], app.logger)
        name = firstname + ' ' + lastname
        with open("config/config.yml") as f:
            config = yaml.safe_load(f)
        company = config['site']['company']
        return render_template('admin.html', error=error, name=name, company=company,  title='admin')

@app.route('/admin/level_management', methods=['GET', 'POST'])
def role_management():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        with open("config/config.yml") as f:
            config = yaml.safe_load(f)
        company = config['site']['company']
        if request.method == 'POST':
            levelId = request.form['userId']
            return redirect(url_for('edit_role',  levelId=levelId))
        else:
            roles = sql.get_table('Role')
            app.logger.info(roles)
            return render_template('role_management.html', error=error, roles=roles, company=company)

@app.route('/admin/level_management/add_role', methods=['GET', 'POST'])
def add_role():
    error = None
    auth_bool = utils.is_auth(session)
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        maxRole = len(sql.get_table('Role'))
        if request.method == 'POST':
            app.logger.info(request.form)
            firstName = request.form['firstname']
            lastName = request.form['lastname']
            email = request.form['email']
            un = request.form['username']
            if sql.get_single_user_info(un):
                error = "Username taken, please choose a  different one"
            pwd = hashing.Hash(request.form['password'])
            phone = request.form['phone']
            phone = re.sub('\D', '', phone)
            role = request.form['stylistlevel']
            if not role.isnumeric():
                error = "Please select a Stylist Level"
            if request.form.get('management'):
                management = 1
            else:
                management = 0
            if error:
             return render_template('add_user_ph.html', error=error, maxRole=maxRole, firstName=firstName, lastName=lastName, 
             email=email, un=un, pwd=pwd, phone=phone, role=role, booth=booth, management=management, company=company)
            else:
                sql.insert_User(firstName, lastName, email, phone, un, pwd, role, management)
            return redirect(url_for('user_management'))
        return render_template('add_user.html', error=error, maxRole=maxRole, company=company)

@app.route('/admin/level_management/<roleId>', methods=['GET', 'POST'])
def edit_role(roleId):
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        with open("config/config.yml") as f:
            config = yaml.safe_load(f)
        company = config['site']['company']
        role = sql.get_all('*','Role',f"roleId = {roleId}")[0]
        if request.method == 'POST':
            role = sql.get_user(roleId)
            app.logger.info(role)
            app.logger.info(request.form)
            if request.form[0]['firstName'] != user['firstName'] :
                sql.update_user(userId,f"firstName = '{request.form['firstName']}'")
            if request.form[0]['lastName'] != user['lastName']:
                sql.update_user(userId,f"lastName = '{request.form['lastName']}'")
            if request.form[0]['phone'] != user['phone']:
                sql.update_user(userId,f"phone = {request.form['phone']}")
            if request.form[0]['email'] != user['email'] :
                sql.update_user(userId,f"email = '{request.form['email']}'")
            if request.form[0]['roleId'] != user['roleId']:
                app.logger.info(f"roleId = {request.form['roleId']}")
                sql.update_user(userId,f"roleId = {request.form['roleId']}")
            if request.form[0].get('management'):
                if request.form[0]['management'] != user['management']:
                    app.logger.info(f"management = {request.form['management']}")
                    sql.update_user(userId,f"management = {request.form['management']}")
            return redirect(url_for('edit_role', roleId=user['roleId']))
        else:
            maxRole = len(sql.get_table('Role'))
            app.logger.info(user)
            return render_template('edit_role.html', error=error, role=role[0], maxRole=maxRole, company=company)


@app.route('/admin/user_management', methods=['GET', 'POST'])
def user_management():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        with open("config/config.yml") as f:
            config = yaml.safe_load(f)
        company = config['site']['company']
        if request.method == 'POST':
            userId = request.form['userId']
            return redirect(url_for('edit_user',  userId=userId))
        else:
            users = sql.get_table('User')
            roles = sql.get_table('Role')
            return render_template('user_management.html', error=error, users=users, roles=roles, company=company)

@app.route('/admin/user_management/<userId>', methods=['GET', 'POST'])
def edit_user(userId):
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        with open("config/config.yml") as f:
            config = yaml.safe_load(f)
        company = config['site']['company']
        user = sql.get_user(userId)[0]
        maxRole = len(sql.get_table('Role'))
        if request.method == 'POST':
            app.logger.info(user)
            app.logger.info(request.form)
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
            if request.form.get('management'):
                if request.form['management'] != user['management']:
                    app.logger.info(f"management = {request.form['management']}")
                    sql.update_user(userId,f"management = {request.form['management']}")
            if error:
                return render_template('edit_user.html', error=error, user=user, maxRole=maxRole, company=company)
            else:
                return redirect(url_for('user_management'))
        else:
            app.logger.info(user)
            return render_template('edit_user.html', error=error, user=user, maxRole=maxRole, company=company)


@app.route('/admin/site_management', methods=['GET', 'POST'])
def site_management():
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        with open("config/config.yml") as f:
            config = yaml.safe_load(f)
        company = config['site']['company']
        if request.method == 'POST':
            with open("config/config.yml") as f:
                config = yaml.safe_load(f)
            startTime = request.form['open']
            endTime = request.form['close']
            config['site']['open'] = startTime
            config['site']['close'] = endTime
            with open("config/config.yml", "w") as f:
                yaml.dump(config, f)
        else:
            with open("config/config.yml") as f:
                config = yaml.safe_load(f)
            app.logger.info(config)
            startTime = config['site']['open']
            endTime = config['site']['close']
        return render_template('site_management.html', error=error, startTime=startTime,
         endTime=endTime, company=company)

@app.route('/admin/user_management/add_user', methods=['GET', 'POST'])
def add_user():
    error = None
    auth_bool = utils.is_auth(session)
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        maxRole = len(sql.get_table('Role'))
        if request.method == 'POST':
            app.logger.info(request.form)
            firstName = request.form['firstname']
            lastName = request.form['lastname']
            email = request.form['email']
            un = request.form['username']
            if sql.get_single_user_info(un):
                error = "Username taken, please choose a  different one"
            pwd = hashing.Hash(request.form['password'])
            phone = request.form['phone']
            phone = re.sub('\D', '', phone)
            role = request.form['stylistlevel']
            if not role.isnumeric():
                error = "Please select a Stylist Level"
            if request.form.get('management'):
                management = 1
            else:
                management = 0
            if error:
             return render_template('add_user_ph.html', error=error, maxRole=maxRole, firstName=firstName, lastName=lastName, 
             email=email, un=un, pwd=pwd, phone=phone, role=role, booth=booth, management=management, company=company)
            else:
                sql.insert_User(firstName, lastName, email, phone, un, pwd, role, management)
            return redirect(url_for('user_management'))
        return render_template('add_user.html', error=error, maxRole=maxRole, company=company)

@app.route('/admin/customer', methods   =['GET', 'POST'])
def customer():
    error = None
    auth_bool = utils.is_auth(session)
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    if not auth_bool:
        return redirect(url_for('login'))
    if request.method == 'POST':
        typeId = request.form['typeId']
        app.logger.info(typeId)
        userId = request.form['userId']
        app.logger.info(f'test: {userId}')
        time = request.form['time']
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        app.logger.info(time)
        if request.form['submit'] == "New Customer":
            return render_template('add_customer.html', error=error, company=company, typeId=typeId, userId=userId, day=day, month=month, year=year, time=time)
        elif request.form['submit'] == "Existing Customer": 
            return render_template('search_customer.html', error=error, company=company, typeId=typeId, userId=userId, day=day, month=month, year=year, time=time)
        elif request.form['submit'] == "Search Customer":
            if request.form['search_type'] == 'Name':
                name = request.form['search'].split()
                if len(name) > 1:
                    customer = sql.get_all('*','Customer',f'(firstName like "%{name[0]}%" and lastName like "%{name[-1]}%") or (firstName like "%{name[-1]}%" and lastName like "%{name[0]}%")')
                elif len(name) == 1:
                    customer = sql.get_all('*','Customer',f'(firstName like "%{name[0]}%") or (lastName like "%{name[0]}%")')
                else:
                    error = "Invalid Input, Please Input a Name"
            elif request.form['search_type'] == 'Phone Number':
                email = request.form['search']
                customer = sql.get_all('*','Customer',f'email = {email}')
            elif request.form['search_type'] == 'Email Address':
                phone = request.form['search']
                customer = sql.get_all('*','Customer',f'phoneNumber = {phone}')
            app.logger.info(customer)
            return render_template('search_customer.html', customers=customer, company=company, typeId=typeId, userId=userId, day=day, month=month, year=year, time=time)
    else:
        pass
        return redirect(url_for('calendarDay', day=day, month=month, year=year))

@app.route('/admin/customer_management', methods=['GET', 'POST'])
def customers():
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:

        return redirect(url_for('login'))
    else:
        customers = sql.get_table('Customer')
        return render_template('customers.html', error=error, customers = customers, company=company)

@app.route('/admin/appointments', methods=['GET', 'POST'])
def appointments():
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        appointments = sql.get_table('AppointmentType')
        return render_template('appointments.html', error=error, appointments = appointments, company=company)

@app.route('/admin/appointments/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        return render_template('add_appointment.html', error=error, company=company)

@app.route('/admin/calendar/', methods=['GET', 'POST'])
def calendar():
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        dt = datetime.today()
        year = dt.year
        month = dt.month
        day = dt.day
        return redirect(url_for('calendarDay', day=day, month=month, year=year))

@app.route('/admin/calendar/<day>-<month>-<year>/book-<userid>', methods   =['GET', 'POST'])
def book(day,month,year,userid):
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        date = f'{year}-{month}-{day}'
        if request.method == 'POST':
            if request.form['time']:
                time = f'{request.form["time"]}'
                app.logger.info(time)
                time = datetime.strptime(time, '%I:%M %p').replace(year=int(year),month=int(month),day=int(day))
                next_appt = sql.get_next_appt(date, time, userid)
                if next_appt:
                    next_appt = next_appt['startTime']
                    app.logger.info(time)
                    app.logger.info(next_appt)
                    maxDur = next_appt - time
                    maxDur = maxDur.total_seconds() / 60
                    app.logger.info(maxDur)
                    where = f'duration < {maxDur} AND hasHourlyRate = 0 ORDER BY 1'
                    appointmentTypes = sql.get_all('typeName, description, duration', 'AppointmentType',where)
                    maxDur = maxDur / 60
                    where = f'duration < {maxDur} AND hasHourlyRate = 1 ORDER BY 1'
                    appointmentTypes += sql.get_all('appointTypeId,typeName, description, duration', 'AppointmentType',where)
                else:
                    appointmentTypes = sql.get_table('AppointmentType')
                return render_template('booking.html', time=time.strftime("%I:%M %p"), day=day, month=month, 
                year=year, appointmentTypes = appointmentTypes, userId = userid, company=company)
            else:
                return redirect(url_for('calendarDay', day=day, month=month, year=year))
        
@app.route('/admin/calendar/<day>-<month>-<year>', methods   =['GET', 'POST'])
def calendarDay(day,month,year):
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        date = datetime(int(year),int(month),int(day),0,0,0)
        if request.method == 'POST':
            if request.form['submit_button'] == 'Month View':
                return redirect(url_for('calendarMonth', month=month, year=year))
            if request.form['submit_button'] == 'Next Day':
                dt = date + timedelta(days=1)
                year = dt.year
                month = dt.month
                day = dt.day
                return redirect(url_for('calendarDay', day=day, month=month, year=year))
            if request.form['submit_button'] == 'Prev Day':
                dt = date - timedelta(days=1)
                year = dt.year
                month = dt.month
                day = dt.day
                return redirect(url_for('calendarDay', day=day, month=month, year=year))
            if request.form['submit_button'] == 'Select Customer':
                typeId = request.form['typeId']
                userId = request.form['userId']
                customerId = request.form['customerId']
                time = request.form['time']
                day = request.form['day']
                month = request.form['month']
                year = request.form['year']
                startTime=f"{ year }-{ month }-{ day } { time }"
                app.logger.info(startTime)
                app.logger.info(userId)
                sql.insert_Appointment(userId, typeId, customerId, "",startTime, app.logger)
                return redirect(url_for('calendarDay', day=day, month=month, year=year))
        else:
            times = []
            formatedtime = date.strftime("%I:%M %p")
            times.append(formatedtime)
            weekday = date.weekday()+1
            day_sql = date.strftime('%Y-%m-%d')
            user_schedule = sql.get_schedule(weekday)
            app.logger.info(user_schedule)
            user_booked = sql.get_bookings(day_sql,app.logger)
            app.logger.info(user_booked)
            for i in range(96): 
                date += timedelta(minutes=15)
                formatedtime = date.strftime("%I:%M %p")
                times.append(formatedtime)
            with open("config/config.yml") as f:
                config = yaml.safe_load(f)
            opentime = config['site']['open']
            closetime = config['site']['close']
            app.logger.info(datetime.strptime(opentime,"%I:%M %p"))
            app.logger.info(datetime.strptime(times[36],"%I:%M %p")) 
            return render_template('Calendar-Day.html', day=day, month=month, year=year,
            times=times,user_schedule=user_schedule, datetime=datetime, 
            user_booked=user_booked, booked = 0, scroll = 'start', opentime = opentime, closetime = closetime, company=company)

@app.route('/admin/calendar/<month>-<year>', methods=['GET', 'POST'])
def calendarMonth(month, year):
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Next Month':
                date = request.form['date']
                date = datetime.strptime(date, '%Y-%m-%d')
                last = date.replace(day = fcalendar.monthrange(date.year, date.month)[1])
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
        lastDay = date.replace(day = fcalendar.monthrange(date.year, date.month)[1]).strftime("%d")
        return render_template('Calendar-Month.html', lastDay = int(lastDay), 
        firstDay=firstDay, day=currentDay, month=currentMonth, 
        year=currentYear, date=date, error=error, company=company)

@app.route('/admin/analysis', methods=['GET', 'POST'])
def analysis():
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    error = None
    auth_bool = utils.is_auth(session)
    if not auth_bool:
        return redirect(url_for('login'))
    else:
        firstname, lastname = sql.get_name(session['user'], app.logger)
        name = firstname + ' ' + lastname
        aptChart = sql.Appiont_by_date('2022-10-18', '2022-10-20')
        return render_template('analysis.html', error=error, aptChart=aptChart, company=company)


@app.route('/logout', methods=['GET'])
def logout():
    session['auth'] = None
    session['user'] = None
    session['level'] = None
    return redirect(url_for('login'))

@app.route('/error')
def error():
    with open("config/config.yml") as f:
        config = yaml.safe_load(f)
    company = config['site']['company']
    return render_template('404.html', title='error page not found', company=company)

if __name__ == "__main__":
    
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(debug=True,host='0.0.0.0')