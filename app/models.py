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

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    username = db.Column(db.String(64), unique=True)  # User 'username': defaults to email if not given
    email = db.Column(db.String(128), unique=True)  # User email: 'toby@gmail.com', 'neko@weeb.com'
    password_hash = db.Column(db.String(128))  # User password hash
    role = db.Column(db.String(64))  # User role: 'Patient', 'Doctor', etc
    phone_number = db.Column(db.String(16))  # User phone number: 555-555-555, 000, etc
    medicare_number = db.Column(db.String(28), unique=True)  # Patient medicare number: 12345678
    provider_number = db.Column(db.String(28), unique=True)  # Provider number: 12345678

    # --- Relationships ---
    centres = db.relationship('Centre', secondary='Works_At')  # Link to centres via intermediary table (many-many)

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


class Centre(db.Model):
    """
    Model representing a Centre and the information associated with it.

    Each centre can have none or many providers working at it. Each provider can work for none or many centres.
    """

    __tablename__ = "Centres"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    type = db.Column(db.String(64))  # Centre "type"? 'Hospital', 'Medical centre', etc
    abn = db.Column(db.Integer, unique=True)  # Centre ABN? 1111, 1112, etc
    name = db.Column(db.String(128), unique=True)  # Centre name? 'USYD Health Shed', 'Heart attac shac' etc
    phone = db.Column(db.String(24))  # Centre phone? '555-555-555', '000', etc
    suburb = db.Column(db.String(64))  # Centre suburb? 'Eastwood', 'Epping', etc

    # --- Relationships ---
    providers = db.relationship('User', secondary='Works_At')  # Link to providers via intermediary table (many-many)

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the Centre instance.
        """

        return '<Centre {}>'.format(self.name)

    def has_providers(self):
        """
        Gets a list of Users that work for this particular Centre instance.

        :return: Returns the providers working for a particular Centre instance.
        """

        return self.providers

    def get_services(self):
        """
        Gets a list of services available from this centre.

        :return: A list of the services available at the Centre.
        """

        # To do this:
        #    - Get all of the providers working at the clinic.
        #    - Query them for distinct roles and sort by ascending
        #    - Return results.

        pass


class WorksAt(db.Model):
    """
    Represents the relationship between the Centre and User table.

    The two foreign key entries link to the primary keys of their respective tables. (email and centre name).
    """

    __tablename__ = "Works_At"

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    place = db.Column(db.String(128), db.ForeignKey('Centres.name'))    # Links to centre
    provider = db.Column(db.String(128), db.ForeignKey('Users.email'))  # Links to provider
    hours_start = db.Column(db.Time())  # Starting hours for provider
    hours_end = db.Column(db.Time())  # Ending hours for provider

    # Relationships
    user = db.relationship(User, backref=db.backref("Works_At", cascade="all, delete-orphan"))
    centre = db.relationship(Centre, backref=db.backref("Works_At", cascade="all, delete-orphan"))

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the WorksAt instance.
        """

        return '<WorksAt {}, {}>'.format(self.email, self.centre)


class Appointment(db.Model):
    """
    Model representing an Appointment and the information associated with it.

    Each Appointment can have exactly 1 provider and 1 patient associated with it.
    """

    __tablename__ = "Appointments"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    patient = db.Column(db.String(128))  # Patient email ( or medicare card? )
    provider = db.Column(db.String(128))  # Provider email ( or provider number? )
    centre = db.Column(db.String(128))  # Centre name
    start_time = db.Column(db.DateTime())  # Start time of appointment
    end_time = db.Column(db.DateTime())  # End time of appointment
    is_confirmed = db.Column(db.Boolean())  # Whether appointment is confirmed or not.
    notes = db.Column(db.String(128))  # Notes from provider

    # --- Relationships ---
    # providers = db.relationship('User', secondary='Works_At')  # Link to providers via intermediary table (many-many)

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the Centre instance.
        """

        return '<Appointment {}, {}>'.format(self.patient, self.provider)


class Prescription(db.Model):
    """
    Model representing a Prescription given during an appointment.

    Many prescriptions can be given by many appointments.
    """

    __tablename__ = "Prescriptions"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    patient = db.Column(db.String(128))  # Patient email ( or medicare card? )
    provider = db.Column(db.String(128))  # Provider email ( or provider number? )
    appointment = db.Column(db.Integer())  # Appointment identifier
    medicine = db.Column(db.String(128))  # Prescribed medicine

    # --- Relationships ---
    # providers = db.relationship('User', secondary='Works_At')  # Link to providers via intermediary table (many-many)

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the Centre instance.
        """

        return '<Prescription {}, {}, {}>'.format(self.patient, self.provider, self.medicine)

class Rating(db.Model):
    """
    Model representing a Rating given by a Patient about either a Centre or Provider.
    """

    __tablename__ = "Ratings"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    type = db.Column(db.String(28))  # Type of rating 'centre' or 'provider'
    patient = db.Column(db.String(128))  # Patient giving the rating
    provider = db.Column(db.String(128))  # Provider email ( or provider number? )
    centre = db.Column(db.String(128))  # Centre name

    # --- Relationships ---
    # providers = db.relationship('User', secondary='Works_At')  # Link to providers via intermediary table (many-many)

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the Centre instance.
        """

        return '<Prescription {}, {}, {}>'.format(self.patient, self.provider, self.medicine)
