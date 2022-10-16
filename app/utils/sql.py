from db import mysql
import utils.hashing as hashing
import pymysql

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

    data = cursor.fetchone()

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
    query = f'SELECT userId, firstName, lastName, TIME_FORMAT(startTime, "%I:%i %p") as  startTime, TIME_FORMAT(endTime, "%I:%i %p") as endTime,dayId  FROM User u JOIN Schedule s on u.userId = s.userId where s.dayId = {weekday} ORDER by u.firstName'
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