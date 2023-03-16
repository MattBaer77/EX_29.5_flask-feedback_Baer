from flask import session, flash

def user_not_logged_in(username):
    print(username)
    if session['username'] != username:
        flash("Please login first!", "danger")
        return True
    return False