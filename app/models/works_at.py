from app import db
from app.models.user import User
from app.models.centre import Centre


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

        :return: A string representation of the WorksAt instance.
        """

        return '<WorksAt {}, {}>'.format(self.email, self.centre)

