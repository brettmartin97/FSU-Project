def is_auth(Session):
    try:
        if type(session['auth']) is bool:
            if session['auth']:
                if not session['admin'] and not session['booth']:
                    return True
                else:
                    if session['admin']:
                        return 2
                    else:
                        return 3
            else:
                return False
        else:
            return False
    except:
        return False

