def setSession(username, code):
    request.session.flush()
    request.session['username'] = username
    request.session['code'] = verification__code
    request.session.set_expiry(300)
    print(f'New session: {request.session["username"]} and {request.session["code"]}')
    return True