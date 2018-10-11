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

    #     child_id = Column(Integer, ForeignKey('child.id'))
    #     child = relationship("Child", back_populates="parent")
    # appointment_id = db.Column(db.Integer, db.ForeignKey('Appointments.id'))
    # appointment.csv = db.relationship('Appointment', back_populates="users")

    # appointments = db.relationship('Appointment', backref='user', lazy='dynamic')

    # company = db.relationship("Company", foreign_keys=[company_id], backref="holders")
    # stakeholder = db.relationship("Company", foreign_keys=[stakeholder_id], backref="holdings")
    # --- Relationships ---
    centres = db.relationship('Centre', secondary='Works_At', lazy='dynamic')  # Link to centres via intermediary table (many-many)

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

        return self.centres.all()

    def calc_rating(self):
        """
        Calculates the average rating for the centre.

        :return: Returns the average rating for the centre.
        """

        num_ratings = 0
        tot_rating = 0
        for r in self.ratings_received:
            num_ratings += 1
            tot_rating += r.rating

        if num_ratings > 0:
            return tot_rating/num_ratings
        else:
            return 0

    @staticmethod
    def do_search(name=None, type=None):
        """
        Performs a sub-search using the provided parameters.
        Returns a list containing each record satisfying given search criteria. (Case insensitive).

        Examples:
        In [1]: User.do_search(name="t")
        Out[2]: [<User tom@gmail.com>, <User toby@gmail.com>, <User thomas@gmail.com>]

        In [3]: User.do_search(name="t", type="path")
        Out[4]: [<User toby@gmail.com>]

        :param name: The username of the user to search for.
        :param type: The 'type' or profession of the user to search for.
        :return: A list of User records matching the given search criteria.
        """

        # Initialise empty list to store search criteria
        criteria = []

        # If search attribute is provided, add it as a search criterion.
        if name: criteria.append(User.username.contains(name))
        if type: criteria.append(User.role.contains(type))

        # Perform search using criteria list and return list of results.
        return User.query.filter(*criteria).all()


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
    providers = db.relationship('User', secondary='Works_At', lazy='dynamic')  # Link to providers via intermediary table (many-many)

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

        return self.providers.all()

    def get_services(self):
        """
        Gets a list of services available from this centre.

        :return: A list of the services available at the Centre.
        """

        # There is probably a far better way of doing this, but I couldn't figure it out. :'(
        services = []
        for r in self.providers.values('role'):
            services.append(r.role)

        return set(services)

    @staticmethod
    def do_search(name=None, type=None, suburb=None):
        """
        Performs a sub-search using the provided parameters.
        Returns a list containing each record satisfying given search criteria. (Case insensitive).

        Examples:
        In [1]: Centre.do_search(name="hosp")
        Out[2]: [<Centre Sydney Children Hospital>,
                 <Centre Prince of Wales Hospital>,
                 <Centre Royal Prince Alfred Hospital>]

        In [3]: Centre.do_search(type="MedicalCentre")
        Out[4]: [<Centre UNSW Health Service>,
                 <Centre USYD Health Service>,
                 <Centre UTS Health Service>]

        :param name: The name of the hospital to search for.
        :param type: The 'type' of hospital.
        :param suburb: The suburb of the hospital to search for.
        :return: A list of Centre records matching the given search criteria.
        """

        # Initialise empty list to store search criteria
        criteria = []

        # If search attribute is provided, add it as a search criterion.
        if name: criteria.append(Centre.name.contains(name))
        if type: criteria.append(Centre.type.contains(type))
        if suburb: criteria.append(Centre.suburb.contains(suburb))

        # Perform search using criteria list and return list of results.
        return Centre.query.filter(*criteria).all()

    def calc_rating(self):
        """
        Calculates the average rating for the centre.

        :return: Returns the average rating for the centre.
        """

        num_ratings = 0
        tot_rating = 0
        for r in self.all_ratings:
            num_ratings += 1
            tot_rating += r.rating

        if num_ratings > 0:
            return tot_rating/num_ratings
        else:
            return 0


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

        return '<WorksAt {}, {}>'.format(self.provider, self.place)


class Appointment(db.Model):
    """
    Model representing an Appointment and the information associated with it.

    Each Appointment can have exactly 1 provider and 1 patient associated with it.
    """

    __tablename__ = "Appointments"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    patient_email = db.Column(db.String(128), db.ForeignKey('Users.email'))
    provider_email = db.Column(db.String(128), db.ForeignKey('Users.email'))
    centre_name = db.Column(db.String(128), db.ForeignKey('Centres.name'))

    start_time = db.Column(db.Time())  # Start time of appointment.csv
    end_time = db.Column(db.Time())  # End time of appointment.csv
    is_confirmed = db.Column(db.Boolean())  # Whether appointment.csv is confirmed or not.
    notes = db.Column(db.String(128))  # Notes from provider

    # --- Relationships ---
    patient = db.relationship("User", foreign_keys=[patient_email], backref='provider_bookings')
    provider = db.relationship("User", foreign_keys=[provider_email], backref='patient_bookings')
    centre = db.relationship("Centre", foreign_keys=[centre_name], backref='all_appointments')

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the Centre instance.
        """

        return "<Appointment: Patient '{}', Provider '{}'>".format(self.patient, self.provider)


class Prescription(db.Model):
    """
    Model representing a Prescription given during an appointment.csv.

    Many prescriptions can be given by many appointments.
    """

    __tablename__ = "Prescriptions"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    patient_email = db.Column(db.String(128), db.ForeignKey('Users.email'))  # Patient email ( or medicare card? )
    provider_email = db.Column(db.String(128), db.ForeignKey('Users.email'))  # Provider email ( or provider number? )
    appointment_id = db.Column(db.Integer(), db.ForeignKey('Appointments.id'))  # Appointment identifier
    medicine = db.Column(db.String(128))  # Prescribed medicine

    # --- Relationships ---
    patient = db.relationship("User", foreign_keys=[patient_email], backref='is_prescribed')
    provider = db.relationship("User", foreign_keys=[provider_email], backref='has_prescribed')
    appointment = db.relationship("Appointment", foreign_keys=[appointment_id], backref='prescription')

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
    rating = db.Column(db.Integer())  # Prescribed medicine
    patient_email = db.Column(db.String(128), db.ForeignKey('Users.email'))  # Patient email ( or medicare card? )
    provider_email = db.Column(db.String(128), db.ForeignKey('Users.email'))  # Provider email ( or provider number? )
    centre_name = db.Column(db.Integer(), db.ForeignKey('Centres.name'))  # Appointment identifier

    # --- Relationships ---
    patient = db.relationship("User", foreign_keys=[patient_email], backref='ratings_given')
    provider = db.relationship("User", foreign_keys=[provider_email], backref='ratings_received')
    centre = db.relationship("Centre", foreign_keys=[centre_name], backref='all_ratings')

    def __repr__(self):
        """
        Specifies the interpreter representation of the object.

        :return: A string representation of the Centre instance.
        """

        return '<Rating {}, {}, {}, {}>'.format(self.type, self.rating, self.provider_email, self.centre_name)
