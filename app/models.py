# models.py
#
# Defines the schema used in our application. We apply a model here as it
# allows us to migrate changes to the database schema without having to
# regenerate the database from scratch.

from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):
    """
    Model representing a User and the information associated with them. This is
    used for user management.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        Returns:
            A string representation of the User instance.
        """

        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
        Generates and stores a hash of a user password. (Using SHA 256).

        Args:
            password (str): The password we're storing a SHA 256 hash of.
        """

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks to see whether see whether a provided plaintext password string
        hashs to our stored password hash.

        Args:
            password (str): The password attempt we're checking with.
        """

        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """
    Returns a User as specified by their User ID. This function is required by
    flask-login.

    Args:
        id (int): The UID used to specify a particular User.
    Returns:
        A User matching a specific UID. If no matches are found, returns None.
    """

    return User.query.get(int(id))
