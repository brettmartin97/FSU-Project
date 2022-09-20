from db import mysql
import utils.hashing as hashing
import pymysql

def get_salt(user):
    query = f'SELECT salt FROM user WHERE username = {user}'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    salt = cursor.fetchone()

    return salt

def set_password(user, password):
    hash = hashing.Hash(password)

    query = f'UPDATE user SET password = {hash} WHERE username = "{user}"'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

def validate_password(user, password, log):
    validationSQL = f'SELECT password FROM user WHERE username = "{user}"'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(validationSQL)

    hashed = cursor.fetchone()['password']
    log.info(hashed)
    salt = hashing.getSalt(hashed)

    hash = hashing.Hash(password, salt)

    query = f'SELECT username FROM user WHERE username = "{user}" and password = "{hash}"'

    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    cursor.execute(query)

    valid = cursor.fetchone()

    return valid