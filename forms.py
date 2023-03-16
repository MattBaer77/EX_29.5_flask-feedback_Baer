from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea


class UserRegistrationForm(FlaskForm):
    """
    username
    password
    email
    first_name
    last_name
    """

    form_name = 'User Registration'
    submit_text = 'Register User'

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):

    form_name = 'Login Form'
    submit_text = 'Login'

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):

    form_name = "Add Feedback"
    submit_text = 'Save Feedback'

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()], widget=TextArea())

