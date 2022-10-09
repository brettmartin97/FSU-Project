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

def get_attribute(user, field, table):
    validationSQL = f'SELECT {field} FROM {table} WHERE username = "{user}"'

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