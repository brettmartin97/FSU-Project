from db import mysql
from io import BytesIO
import utils.hashing as hashing
import pymysql  
import pandas as pd
import matplotlib.pyplot as plt
import base64

def set_password(user, password):
    hash = hashing.Hash(password)

    query = f'UPDATE User SET password = {hash} WHERE username = "{user}"'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    conn.close()

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

def run_query(query):
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query)

    data = cursor.fetchall()

    return data

def run_update(update):

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(update)

    conn.commit()

    return True

def chart_data():

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    df = pd.read_sql(query, con)

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


def get_customer(id):
    query = f'SELECT * FROM Customer WHERE customerId = {id}'

    return run_query(query)

def get_user(id):
    query = f'SELECT * FROM User WHERE userId = {id}'

    return run_query(query)

def get_user_role():
    query = f'SELECT * FROM User as u, Role as r WHERE u.roleId = r.roleId'

    return run_query(query)

def get_user_role(id):
    update = f'SELECT * FROM User as u, Role as r WHERE u.roleId = r.roleId and u.userId = {id}'

    return run_update(update)

def update_user(id, update):
    query = f'UPDATE User SET {update} WHERE userId = {id}'

    return run_update(query)

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


# Insert data into Schedule table.
def insert_Role(rName,com,hRate):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'''INSERT INTO Role(roleName, commission, hourlyRate) 
            VALUES (%s, %s, %s)'''


    cursor.execute(query, (rName,com,hRate))

    conn.commit()

    return True



"""
Fixed this insert function.
The isMan variable needs to be a 0 for False or a 1 for True.
userId is ignored since it auto increments.

-Hayden
"""
def insert_User(fName,lName,email,phone,username,password,roleId,isMan):

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

# Insert data into Schedule table.
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


# Insert data into AppointmentType table, hourly rate must be a 0 for False or a 1 for True for insertion.
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


# Insert data into Schedule table.
def insert_Pricing(aTypeId, rId, pri):
    
    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f'''INSERT INTO Pricing(appointTypeId, roleId, price) 
            VALUES (%s,  %s, %s)'''


    cursor.execute(query, (aTypeId, rId, pri))

    conn.commit()

    return True


# Insert data into Customer table.
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
Gets the data for the charts using the SQL
"""
def chart_data(query):

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    df = pd.read_sql(query, conn)

    return df

def build_barchart(title, x, y):
    plt.close
    plt.title(title)
    plt.bar(x, y)
    plt.xticks(rotation=75)

    img = BytesIO()

    plt.savefig(img, format ='png')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')

    return plotUrl

"""
Gets the total number of appointments within the time frame.
"""
def appointment_total(startDay, endDay):
    query = f'''SELECT count(appointId) as num
    FROM Appointment
    WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}'
    '''
    
    data = chart_data(query)

    appoint = data['num']

    return appoint[0]


"""
Creates a chart for showing appointment by date.
"""
def Appiont_by_date(startDay, endDay):
    startDay = '2022-10-18'
    endDay = '2022-10-20'
    query = f'''SELECT date(startTime) as d, count(date(startTime)) as num 
    FROM Appointment
    WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' 
    GROUP BY d 
    ORDER BY d ASC'''

    data = chart_data(query)
    
    plt.close()
    plt.title('Appointment by date')
    plt.bar(data.d, data.num)
    plt.xticks(rotation=75)

    img = BytesIO()

    plt.savefig(img, format ='png')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')

    return plotUrl

"""
Creates a chart for showing filtered appointment by user and grouped by date.
"""
def Appiont_by_user(Id, startDay, endDay):
    query = f'''SELECT date(startTime) as d, count(date(startTime)) as num 
    FROM Appointment
    WHERE date(startTime) >= '{startDay}' and date(startTime) <= '{endDay}' and userId = {Id} 
    GROUP BY d 
    ORDER BY d ASC'''

    data = chart_data(query)

    #data['d'] = pd.to_datetime(data['d'], format = '%Y-%m-%d')
    plt.close()
    plt.title('Appointment by date')
    plt.bar(data.d, data.num)
    plt.xticks(rotation=75)

    img = BytesIO()

    plt.savefig(img, format ='png')
    plotUrl = base64.b64encode(img.getvalue()).decode('utf8')

    return plotUrl





