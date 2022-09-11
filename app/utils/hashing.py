from ast import Constant
import hashlib
import os

SALT_LEGTH = 32

def Hash(self, unecoded):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    