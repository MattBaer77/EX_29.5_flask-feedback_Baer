from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserRegistrationForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from user_not_logged_in import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET - Show a form to register a new user
    POST - Handle a form to register a new user
    """
    # If userID in session - consider sending to different location

    form = UserRegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
        
        except IntegrityError:
            form.username.errors.append('One or more field already taken')
            return render_template('register.html', form=form)

        session['username'] = new_user.username

        flash('Welcome! Successfully Created Your Account!', "success")

        return redirect(f'/users/{username}')

    else:

        return render_template("register.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    """
    GET - Show a form that when submitted will login a user. Form accepts username and password
    POST - Process login form, ensuring the user is authenticated and going to /secret if authenticated
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        login_user = User.authenticate(username, password)

        if login_user:
            flash(f"Welcome Back, {login_user.username}!", "primary")
            session['username'] = login_user.username
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')

# @app.route('/secret')
# def secret():

#     if user_not_logged_in():
#         return redirect('/login')

#     return render_template("secret.html")

@app.route('/users/<username>')
def user_details(username):

    if user_not_logged_in(username):
        print('Not Logged In')
        return redirect('/login')

    user = User.query.get_or_404(username)

    # raise

    return render_template("user-details.html", user=user)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):

    if user_not_logged_in(username):
        return redirect('/login')

    user = User.query.get_or_404(username)

    if user.username == session['username']:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted!", "info")
        return redirect('/login')

    flash("You don't have permission to do that!", "danger")
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    
    if user_not_logged_in(username):
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)

        try:
            db.session.commit()
        except IntegrityError:
            form.feedback.errors.append('Could not save your feedback')
            return render_template('/login')

        return redirect(f'/users/{username}')

    return render_template('feedback.html', form=form)

@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):

    feedback = Feedback.query.get_or_404(id)

    if user_not_logged_in(feedback.username):
        return redirect('/login')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{feedback.username}')

    return render_template('feedback.html', form=form)