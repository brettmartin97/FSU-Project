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

    query = f'UPDATE User SET password = {hash} WHERE username = "{user}"'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    conn.close()

"""
Validate that the password of a user is hashed.
"""
def validate_password(user, password, log):
    validationSQL = f'SELECT password FROM User WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    hashed = cursor.fetchone()['password']
    log.info(hashed)
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
def get_attribute(field, table, where):
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
Called by other functions to chart data.
"""
def chart_data():

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    df = pd.read_sql(query, con)

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
def get_user_role():
    query = f'SELECT * FROM User as u, Role as r WHERE u.roleId = r.roleId'

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
def get_bookings(date):
    query = f'''SELECT userId, TIME_FORMAT(startTime, "%I:%i %p") as startTime,
    CASE 
    WHEN at.hasHourlyRate THEN TIME_FORMAT(TIME(DATE_ADD(a.startTime, INTERVAL at.duration HOUR)), "%I:%i %p") 
    ELSE TIME_FORMAT(TIME(DATE_ADD(a.startTime, INTERVAL at.duration MINUTE)), "%I:%i %p") 
    END as endTime, at.appointTypeId, at.description
    FROM Appointment a JOIN AppointmentType at on a.appointTypeId = at.appointTypeId where startTime between '{date} 00:00:00' and '{date} 23:59:59' ORDER by a.userID'''
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
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
    print(fName,lName,email,phone,username,password,roleId,isMan, flush=True)

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
    print(dId, uId, sTime, endTime, flush=True)

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
    print(tName, des, dur, hHourlyRate, flush=True)

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
    print(aTypeId, rId, pri, flush=True)

    query = f'''INSERT INTO Pricing(appointTypeId, roleId, price) 
            VALUES (%s,  %s, %s)'''


    cursor.execute(query, (aTypeId, rId, pri))

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
    print(fName, lName, mail, pNumber, flush=True)

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
def insert_Appointment(uId, apptId, cusId, note, sTime):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'SELECT roleId FROM User WHERE userId = {uId}'
    cursor.execute(query)
    temp = cursor.fetchone()
    rId = temp['roleId']

    query = f'SELECT totalPriceId FROM Pricing WHERE appointTypeId = {apptId} AND roleId = {rId}'
    cursor.execute(query)
    temp2 = cursor.fetchone()
    tPId = temp2['totalPriceId']

    print(uId, apptId, cusId, tPId, note, sTime, flush=True)

    query = f'''INSERT INTO Appointment(userId, appointTypeId, customerId, totalPriceId, notes, startTime) 
            VALUES (%s, %s, %s, %s, %s, %s)'''


    cursor.execute(query, (uId, apptId, cusId, tPId, note, sTime))

    conn.commit()

    return True


"""
Gets the data for the charts using the SQL
"""
def chart_data(query):

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    df = pd.read_sql(query, conn)

    return df
"""
Builds the appointment Chart
"""
def appointment_chart():
    query = f'''SELECT count(a.appointID) as appointments, at.typeName 
    FROM Appointment as a, AppointmentType as at 
    WHERE a.appointTypeId = at.appointTypeId GROUP BY typeName'''

    data = chart_data(query)
    
    plt.title('Customers by Appointment Type')
    plt.bar(data.typeName, data.appointments)
    plt.xticks(rotation=75)

    img = BytesIO()

    plt.savefig(img, format ='png')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')

    return plotUrl    









