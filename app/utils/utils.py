def is_auth(session):
    if len(session) != 0:
        if session['auth']:
            if not session['admin'] and not session['auth']:
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

