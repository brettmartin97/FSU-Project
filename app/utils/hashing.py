import bcrypt

SALT_LEGTH = 32

def Hash(unencoded, salt = None):
    encoded = unencoded.encode('UTF-8')
    if not salt:
        salt = bcrypt.gensalt()
    else:
        salt = salt.encode('UTF-8')
    # Hashing the password
    hashed = bcrypt.hashpw(encoded, salt)
    
    return hashed.decode('UTF-8')

def getHash(value):
    val = value[29::]
    return (val)

def getSalt(value):
    val = value[:29:]
    return (val)

#print (Hash("testing"))