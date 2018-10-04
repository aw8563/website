# models.py
#
# Defines the schema used in our application. We apply a model here as it
# allows us to migrate changes to the database schema without having to
# regenerate the database from scratch.

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

    def works_at(self):
        """
        Ayy lmao
        TODO: Write me
        :return:
        """

        return


class Centre(db.Model):
    """
    Model representing a Centre and the information associated with it.

    Each centre can have none or many providers working at it. Each provider can work for none or many centres.
    """

    __tablename__ = "Centres"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    abn = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(24))
    suburb = db.Column(db.String(64))

    # Relationships
    providers = db.relationship('User', secondary='Works_At')

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        Returns:
            A string representation of the Centre instance.
        """

        return '<Centre {}>'.format(self.name)


class WorksAt(db.Model):
    """
    Represents the relationship between the Centre and User table.

    The two foreign key entries link to the primary keys of their respective tables. (email and centre name).
    """

    __tablename__ = "Works_At"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(128), db.ForeignKey('Centres.name'))
    provider = db.Column(db.String(128), db.ForeignKey('Users.email'))

    # Relationships
    user = db.relationship(User, backref=db.backref("Works_At", cascade="all, delete-orphan"))
    centre = db.relationship(Centre, backref=db.backref("Works_At", cascade="all, delete-orphan"))

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        Returns:
            A string representation of the WorksAt instance.
        """

        return '<WorksAt {}, {}>'.format(self.email, self.centre)


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
