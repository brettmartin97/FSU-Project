from db import mysql
import utils.hashing as hashing
import pymysql

def set_password(user, password):
    hash = hashing.Hash(password)

    query = f'UPDATE user SET password = {hash} WHERE username = "{user}"'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    conn.close()

def validate_password(user, password, log):
    validationSQL = f'SELECT password FROM user WHERE username = "{user}"'

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

    query = f'SELECT username FROM user WHERE username = "{user}" and password = "{hash}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    valid = cursor.fetchone()

    conn.close()

    return valid

def get_role(user):
    validationSQL = f'SELECT role FROM user WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    role = cursor.fetchone()['role']

    conn.close()

    return role


def get_name(user, log):
    query = f'SELECT firstName, lastName FROM user WHERE username = "{user}"'

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




def get_user_info(user):
    query = f'SELECT * FROM user WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
                           user='root',
                           password="root",
                           db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query)

    sqlInfo = cursor.fetchone()
    info = list()

    info.append(sqlInfo['userID'])
    info.append(sqlInfo['firstName'])
    info.append(sqlInfo['lastName'])
    info.append(sqlInfo['email'])
    info.append(sqlInfo['phone'])
    info.append(sqlInfo['username'])
    info.append(sqlInfo['role'])

    conn.close()
    print(info)

    return info


def get_email(user):
    query = f'SELECT email FROM user WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(query)

    email = cursor.fetchone()['email']

    conn.close()
    print(email)

    return email

def get_id(user):
    query = f'SELECT usrID FROM user WHERE username = "{user}"'

    conn = pymysql.connect(host='db',
        user='root', 
        password = "root",
        db='fsu')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(query)

    id = cursor.fetchone()['id']

    conn.close()

    print(id)

    return id