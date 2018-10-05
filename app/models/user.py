
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    """
    Model representing a User and the information associated with them. This is
    used for user management.

    This user represents both patients and other types of doctors.
    Each user can work at none or many centres, and a centre and have none or many users working in it.
    """

    __tablename__ = "Users"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))

    # Relationships
    centres = db.relationship('Centre', secondary='Works_At')

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the User instance.
        """

        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
        Generates and stores a salted hash of a user password. (Using SHA 256).

        :param password: The password we're setting for a user.
        :return: None
        """

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks to see whether see whether a provided plaintext password string
        hashs to our stored password hash.

        :param password: The password attempt we're checking with.
        :return: True, if the password matches, False otherwise.
        """

        return check_password_hash(self.password_hash, password)

    def works_at(self):
        """
        Gets a list of Centres a particular User instance works at.

        :return: A list of Centres this User works at, if None, returns and empty list.
        """

        return self.centres


@login.user_loader
def load_user(id):
    """
    Returns a User as specified by their User ID. This function is required by
    flask-login.

    :param id: The UID used to specify a particular User.
    :return: A User matching a specific UID. If no matches are found, returns None.
    """

    return User.query.get(int(id))
