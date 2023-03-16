from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserRegistrationForm, LoginForm
from sqlalchemy.exc import IntegrityError

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

        return redirect('/secret')

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
            return redirect('/secret')

        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

    return render_template("login.html", form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/secret')
def secret():

    if 'username' not in session:
        flash(f"Please login first!", "danger")
        return redirect('/login')

    return render_template("secret.html")

@app.route('/users/<username>')
def user_details(username):

    if 'username' not in session:
        flash(f"Please login first!", "danger")
        return redirect('/login')

    user = User.query.get_or_404(username)
    
    return render_template("user-details.html", user=user)

