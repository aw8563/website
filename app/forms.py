# forms.py
#
# This file contains class definitions for web forms to be used in our UI. This
# file exists for two main purposes:
#     1). For separation and abstraction of web forms.
#     2). To allow us to easily instantiate new forms as we require them.

from app.models import User
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class LoginForm(FlaskForm):
    """
    Form used to collect login credentials, as well as the user's "remember me"
    preference.
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    """
    Form used to register a new account. Collects and validates the information
    required in order to make an account.
    """

    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=128)
        ])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3,max=64)
        ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=3,max=64)
        ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
        ])

    submit = SubmitField('Sign up!')

    def validate_email(self, email):
        """
        This method checks to see whether the provided email is already taken
        by another user.

        If successful, returns nothing, otherwise, raises a ValidationError.

        Args:
            email (str): The email we're checking for already being used.
        Returns:
            Nothing, if successful.
        Raises:
            ValidationError: If the email address is already in use.
        """

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
            'This email address is already in-use, please choose another.')

    def validate_username(self, username):
        """
        This method checks to see whether the provided username is already
        taken by another user.

        If successful, returns nothing, otherwise, raises a ValidationError

        Args:
            username (str): The username we're checking for already being used.
        Returns:
            Nothing, if successful.
        Raises:
            ValidationError: If the username is already in use.
        """

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
            'This username is already in-use, please choose another.')
