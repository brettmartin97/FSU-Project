def is_auth(session):
    try:
        if type(session['auth']) is bool:
            if session['auth']:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

