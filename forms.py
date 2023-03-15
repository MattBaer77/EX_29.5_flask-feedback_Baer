from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired

class RegistrationForm(FlaskForm):
    """
    username
    password
    email
    first_name
    last_name
    """

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Username", validators=[InputRequired()])
    email = EmailField("Username", validators=[InputRequired()])
    first_name = StringField("first_name", validators=[InputRequired()])
    last_name = StringField("last_name", validators=[InputRequired()])

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Username", validators=[InputRequired()])