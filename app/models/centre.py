
from app import db


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

        :return: A string representation of the Centre instance.
        """

        return '<Centre {}>'.format(self.name)

    def has_providers(self):
        """
        Gets a list of Users that work for this particular Centre instance.

        :return: Returns the providers working for a particular Centre instance.
        """

        return self.providers
