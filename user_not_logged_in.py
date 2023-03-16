from flask import session, flash

def user_not_logged_in():
    if "username" not in session:
        flash("Please login first!", "danger")
        return True
    return False