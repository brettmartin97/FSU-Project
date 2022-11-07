from db import mysql
from io import BytesIO
import utils.hashing as hashing
import pymysql  
import pandas as pd
import matplotlib.pyplot as plt
import base64


"""
Hashes the password of the specified user.
"""
def set_password(user, password):

    hash = hashing.Hash(password)

    query = f'UPDATE User SET password = "{hash}" WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    conn.commit()

    conn.close()

"""
Validate that the password of a user is hashed.
"""
def validate_password(user, password):
    validationSQL = f'SELECT password FROM User WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    hashed = cursor.fetchone()['password']
    
    salt = hashing.getSalt(hashed)

    hash = hashing.Hash(password, salt)

    query = f'SELECT username FROM User WHERE username = "{user}" and password = "{hash}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    valid = cursor.fetchone()

    conn.close()

    return valid

"""
Get data from a specified table.
"""
def get_attribute_single(field, table, where):
    validationSQL = f'SELECT {field} FROM {table} WHERE {where}'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    attribute = cursor.fetchone()[field]

    conn.close()

    return attribute

"""
Get all data of a field from a specified table.
"""
def get_attribute_all(field, table, where):
    validationSQL = f'SELECT {field} FROM {table} WHERE {where}'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    attribute = cursor.fetchall()[field]

    conn.close()

    return attribute

"""
Get all data from a specified table.
"""
def get_all(field, table, where):
    validationSQL = f'SELECT {field} FROM {table} WHERE {where}'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    attribute = cursor.fetchall()

    conn.close()

    return attribute


"""
Get the first and last name of a user from the User table.
"""
def get_name(user, log):
    query = f'SELECT firstName, lastName FROM User WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(query)
    #log.info(cursor.fetchone())
    name = cursor.fetchone()
    firstName = name['firstName']
    lastName = name['lastName']

    conn.close()
    
    return firstName, lastName

"""
Get the data of a single user from the User table.
"""
def get_single_user_info(user):
    query = f'SELECT * FROM User WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query)

    sqlInfo = cursor.fetchone()

    return sqlInfo

"""
Get the data of a single role from the Role table.
"""
def get_single_role_info(rName):
    query = f'SELECT * FROM Role WHERE roleName = "{rName}"'

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query)

    sqlInfo = cursor.fetchone()

    return sqlInfo

"""
Called by other functions to run specified query.
"""
def run_query(query):
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query)

    data = cursor.fetchall()

    return data

"""
Called by other functions to run specified update query.
"""
def run_update(update):

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(update)

    conn.commit()

    return True


"""
Gets all data from a table in specified order.
"""
def get_table(table, order=1):
    query = f'SELECT * FROM {table} ORDER by {order}'
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    return data
    
"""
Get data of specific customer.
"""
def get_customer(id):
    query = f'SELECT * FROM Customer WHERE customerId = {id}'

    return run_query(query)

"""
Get data of specific user.
"""
def get_user(id):
    query = f'SELECT * FROM User WHERE userId = {id}'

    return run_query(query)

"""
Gets the role assigned to a user.
"""
def get_user_role(id):
    query = f'SELECT * FROM User as u, Role as r WHERE u.roleId = r.roleId and userId = {id}'

    return run_query(query)

"""
Gets the role assigned to a user specified by their ID.
"""
def get_user_role(id):
    update = f'SELECT * FROM User as u, Role as r WHERE u.roleId = r.roleId and u.userId = {id}'

    return run_update(update)

"""
Updates user data.
"""
def update_user(id, update):
    query = f'UPDATE User SET {update} WHERE userId = {id}'

    return run_update(query)

"""
Update data in specified table.

Example call in rest.py:
sql.update_table('Customer', 'firstName = "Auxton"', 'customerId = 1')
"""
def update_table(table, update, where):
    query = f'UPDATE {table} SET {update} WHERE {where}'

    return run_update(query)

"""
Delete data in specified table.

Example call in rest.py:
sql.delete_data('Customer', 'customerId = 1')
"""
def delete_data(table, where):
    query = f'DELETE FROM {table} WHERE {where}'

    return run_update(query)

"""
Get the schedule of a user.
"""
def get_schedule(weekday):
    query = f'SELECT u.userId, u.firstName, u.lastName, TIME_FORMAT(startTime, "%I:%i %p") as  startTime, TIME_FORMAT(endTime, "%I:%i %p") as endTime,dayId  FROM User u JOIN Schedule s on u.userId = s.userId where s.dayId = {weekday} ORDER by u.firstName'
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

"""
Get the booking data.
"""
def get_bookings(date, logger):
    query = f'''SELECT userId, TIME_FORMAT(startTime, "%I:%i %p") as startTime,
    CASE 
    WHEN at.hasHourlyRate THEN TIME_FORMAT(TIME(DATE_ADD(a.startTime, INTERVAL at.duration HOUR)), "%I:%i %p") 
    ELSE TIME_FORMAT(TIME(DATE_ADD(a.startTime, INTERVAL at.duration MINUTE)), "%I:%i %p") 
    END as endTime, at.appointTypeId, at.description
    FROM Appointment a JOIN AppointmentType at on a.appointTypeId = at.appointTypeId where startTime between '{date} 00:00:00' and '{date} 23:59:59' ORDER by a.userID'''
    
    logger.info(query)
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    return data


"""
Get the next appointment.
"""
def get_next_appt(date, time, userid):
    query = f'''SELECT userId, at.duration, a.startTime
    FROM Appointment a JOIN AppointmentType at on a.appointTypeId = at.appointTypeId 
    WHERE startTime > '{time}' and userId = {userid}
    ORDER by a.startTime'''
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchone()
    return data


"""
Insert data into Role table.

The hGoal variable needs to be a 0 for False or a 1 for True.

Example call in rest.py:
sql.insert_Role('Secret Stylist', '99%', 0, 0)
"""
def insert_Role(rName, com, hRate, hGoal):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(rName, com, hRate, hGoal, flush=True)

    query = f'''INSERT INTO Role(roleName, commission, hourlyRate, hasGoal) 
            VALUES (%s, %s, %s, %s)'''


    cursor.execute(query, (rName, com, hRate, hGoal))

    conn.commit()

    return True


"""
Insert data into RoleGoal table.

Example call in rest.py:
sql.insert_RoleGoal(10, 'Amount of Money Earned:', 15.00)
"""
def insert_RoleGoal(rId, gName, val):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(rId, gName, val, flush=True)

    query = f'''INSERT INTO RoleGoal(roleId,goalName, value) 
            VALUES (%s, %s, %s)'''


    cursor.execute(query, (rId, gName, val))

    conn.commit()

    return True


"""
Insert data into User table.

Need to add hashing step for password insertion.

The isMan variable needs to be a 0 for False or a 1 for True.

Example call in rest.py:
sql.insert_User('Diane2', 'Temp4-2','temp4-2@gmail.com',222111333,'diane2','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 4, 0)
"""
def insert_User(fName, lName, email, phone, username, password, roleId, isMan):

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'''INSERT INTO User(firstName, lastName, email, phone, username, password, roleId, management) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''


    cursor.execute(query, (fName,lName,email,phone,username,password,roleId,isMan))

    conn.commit()

    return True    


"""
Insert data into Schedule table.

Example call in rest.py:
sql.insert_Schedule(1,2, '09:55:22', '17:55:22')
"""
def insert_Schedule(dId, uId, sTime, endTime):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'''INSERT INTO Schedule(dayId, userId, startTime, endTime) 
            VALUES (%s, %s, %s, %s)'''


    cursor.execute(query, (dId, uId, sTime, endTime))

    conn.commit()

    return True


"""
Insert data into AppointmentType table.

The hHourlyRate variable needs to be a 0 for False or a 1 for True.

Example call in rest.py:
sql.insert_AppointmentType('ShagEX', 'DescTemp20', 35, 0)
"""
def insert_AppointmentType(tName, des, dur, hHourlyRate):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'''INSERT INTO AppointmentType(typeName, description, duration, hasHourlyRate) 
            VALUES (%s, %s, %s, %s)'''


    cursor.execute(query, (tName, des, dur, hHourlyRate))

    conn.commit()

    return True


"""
Insert data into Pricing table.

Example call in rest.py:
sql.insert_Pricing(16, 12, 77.00)
"""
def insert_Pricing(aTypeId, rId, pri):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    for i in range(0,len(pri)):

        query = f'''INSERT INTO Pricing(appointTypeId, roleId, price) 
                VALUES ({aTypeId}, {rId[i]}, {pri[i]})'''


        cursor.execute(query)

    conn.commit()

    return True


"""
Insert data into Customer table.

Example call in rest.py:
sql.insert_Customer('Austin22', 'Custemp22','custemp22@gmail.com', 222)
"""
def insert_Customer(fName, lName, mail, pNumber):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'''INSERT INTO Customer(firstName, lastName, email, phoneNumber) 
            VALUES (%s, %s, %s, %s)'''


    cursor.execute(query, (fName, lName, mail, pNumber))

    conn.commit()

    return True


"""
Insert data into Appointment table.

Example call in rest.py:
sql.insert_Appointment(5, 2, 15, 'Baked in Temp Appointment34', '2022-10-17 09:33:33')
"""
def insert_Appointment(uId, apptId, cusId, note, sTime,logger):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT roleId FROM User WHERE userId = {uId}"
    
    logger.info(query)
    cursor.execute(query)
    temp = cursor.fetchone()
    rId = temp['roleId']

    query = f'SELECT totalPriceId FROM Pricing WHERE appointTypeId = {apptId} AND roleId = {rId}'
    
    logger.info(query)
    cursor.execute(query)
    temp2 = cursor.fetchone()
    tPId = temp2['totalPriceId']

    print(uId, apptId, cusId, tPId, note, sTime, flush=True)

    query = f'''INSERT INTO Appointment(userId, appointTypeId, customerId, totalPriceId, notes, startTime) 
            VALUES (%s, %s, %s, %s, %s, %s)'''

    logger.info(query)

    cursor.execute(query, (uId, apptId, cusId, tPId, note, sTime))

    conn.commit()

    return True

"""
Puts a mySQl query into a pandas datafram

Pass the query to the function and it will return the dataframe

Example call in rest.py:
sql.chart_data(f'Select * FROM Appointments')
"""
def chart_data(query):
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    df = pd.read_sql(query, conn)

    return df

"""
Creates a bar chart or line chart

Pass the the datafram columns to the function, put 
True for line if want the chart to be a line chart

Example call in rest.py:
sql.build_barchart(data.days, data.sales) or sql.build_barchart(data.days, data.sales, line = True)
"""
def build_barchart(title, x, y, line = None):
    plt.clf()
    plt.title(title)
    #  x = pd.to_datetime(x).dt.normalize()
    plt.bar(x, y)
    plt.xticks(rotation=75)
    plt.gray()

    img = BytesIO()

    plt.savefig(img, format='png', cmap='grayscale')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')

    return plotUrl


"""
Creates a pie chart

Pass the the datafram columns to the function and labels as the y columns

Example call in rest.py:
sql.build_piechart('Appointments', data.appointments, data.typeName)
"""
def build_piechart(title, x, l):
    plt.clf()
    plt.title(title)
    plt.pie(x, labels=l)
    plt.xticks(rotation=75)

    img = BytesIO()

    plt.savefig(img, format='png')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')

    return plotUrl


# Gets the total number of appointments within the time frame.
def total_appointments(startDay, endDay, id = None):
    if not id:
        query = f'''SELECT appointId
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}'
        '''
    else:
        query = f'''SELECT appointId, userId
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id}
        '''

    data = chart_data(query)

    totalAppoint =  0
    totalAppoint = len(data.appointId)
    print(totalAppoint, flush=True)

    return totalAppoint


# Creates a chart for showing appointment by date.
def appointment_by_date(startDay, endDay, id=None):
    if not id:
        query = f'''SELECT DATE_FORMAT(startTime, '%Y-%m-%d') as d, count(date(startTime)) as num 
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' 
        GROUP BY d 
        ORDER BY d ASC'''
        data = chart_data(query)
        plt.close()
        plotUrl = build_barchart('Appointment by date', data.d, data.num)
    else:
        query = f'''SELECT DATE_FORMAT(startTime, '%Y-%m-%d') as d, count(date(startTime)) as num, userId
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id} 
        GROUP BY d 
        ORDER BY d ASC'''

        data = chart_data(query)
        plt.clf()
        plotUrl = build_barchart('Appointment by date', data.d, data.num)

    return plotUrl


# pie chart that shows appointment type for managment.
def appointmentType_chart(startDay, endDay, id=None):
    if not id:
        query = f'''SELECT a.appointTypeId as appoint, count(a.appointId) as c
        FROM Appointment as a, AppointmentType as t
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and a.appointTypeId = t.appointTypeId
        GROUP BY a.appointTypeId'''
        data = chart_data(query)
        print(data, flush = True)
        plt.clf()
        plotUrl = build_piechart('Appointment Types', data.c, data.appoint)
    else:
        query = f'''SELECT a.appointTypeId as appoint, count(a.appointId) as c
        FROM Appointment as a, AppointmentType as t
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id} and a.appointTypeId = t.appointTypeId
        GROUP BY a.appointTypeId'''
        data = chart_data(query)
        print(data, flush = True)
        plt.clf()
        plotUrl = build_piechart('Appointment Types', data.c, data.appoint)

    return plotUrl


def customer_chart(startDay, endDay, id=None):
    if not id:
        query = f'''SELECT DATE_FORMAT(startTime, '%Y-%m-%d') as d, count(DISTINCT(customerId)) as cust
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' 
        GROUP BY DATE_FORMAT(startTime, '%Y-%m-%d')
        ORDER BY d ASC'''
        data = chart_data(query)
        print(data, flush = True)
        plt.clf()
        plotUrl = build_barchart('Customers by date', data.d, data.cust)
    else:
        query = f'''SELECT DATE_FORMAT(startTime, '%Y-%m-%d') as d, count(DISTINCT(customerId)) as cust, userId
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id} 
        GROUP BY DATE_FORMAT(startTime, '%Y-%m-%d')
        ORDER BY d ASC'''
   
        data = chart_data(query)
        print(data, flush = True)
        plt.clf()
        plotUrl = build_barchart('Customers by date', data.d, data.cust)
    

    return plotUrl


def percentage_prebooked(startDay, endDay, id):
    queryOne = f'''SELECT count(*) as cust, customerId
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id}
        GROUP BY customerId 
        HAVING cust >= 2'''

    queryTwo = f'''SELECT count(*) as cust, customerId, userId
        FROM Appointment
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id}
        GROUP BY customerId 
                '''
    dataOne = chart_data(queryOne)
    dataTwo = chart_data(queryTwo)

    percPreBooked = (len(dataOne.cust) / len(dataTwo.cust)) * 100

    return percPreBooked

def total_sales(startDay, endDay, id = None):
    if not id:
        query = f'''SELECT DATE_FORMAT(startTime, '%Y-%m-%d') as d, SUM(p.price) as sales
        FROM Appointment as a, Pricing as p
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and a.totalPriceId = p.totalPriceId 
        GROUP BY DATE_FORMAT(startTime, '%Y-%m-%d')
        ORDER BY d ASC'''    
    else:
        query = f'''SELECT DATE_FORMAT(startTime, '%Y-%m-%d') as d, SUM(p.price) as sales, a.userId
        FROM Appointment as a, Pricing as p
        WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {id} and a.totalPriceId = p.totalPriceId 
        GROUP BY DATE_FORMAT(startTime, '%Y-%m-%d')
        ORDER BY d ASC'''
    data = chart_data(query)

    plt.clf()
    fig, ax = plt.subplots()
    plt.style.use('grayscale')
    ax.plot(data.d, data.sales)
       
    ax.yaxis.set_major_formatter('${x:1.2f}')
    plt.title("Total Sales")
    plt.xticks(rotation=75)
 
    img = BytesIO()

    plt.savefig(img, format='png')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')
    
    return plotUrl