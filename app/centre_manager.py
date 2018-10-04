# centre_manager.py
#
# This file is responsible for centre management and otherwise interacting with centres.

import logging

from termcolor import colored

from app import db
from app.models import Centre


class CentreManager:
    """
    Class which is responsible for Centre management for the Medi-soft HCS. Namely, it provides abstraction for:
        - Centre creation.
        - Centre deletion.

    Largely, it does this by querying the Medi-soft Sqlite3 backend and maintaining a queriable list of records.
    """

    def __init__(self):
        """
        Constructor for CentreManager class.

        Initialises a list of Centres from all existing Centre records.
        """

        # Initialise CentreManager attributes.
        self._logger = logging.getLogger(__name__)

        # Load all existing users from database.
        self._centres = self._load_centres()

        # Indicate successful creation of HCS.
        self._logger.debug(colored("Initialised new CentreManager.", 'yellow'))

    def _load_centres(self):
        """
        Queries the database and returns all centre records as a list. Used to initialise the class upon creation.

        :return: A list of records for each Centre.
        """
        self._logger.info(colored('Loading existing centres.', 'yellow'))
        centres = Centre.query.all()
        self._logger.info(colored('Loaded centres: %s' % centres, 'green'))

        return centres

    def add_centre(self, type, abn, name, phone, suburb):
        """
        Creates a new Centre and adds it to the Centre database. If successful, also appends new Centre to current
        centres list.

        :param type: The type of centre. ('Hospital', 'Medical centre', 'Shed', etc).
        :param abn: The ABN of the centre. This must be unique.
        :param name: The name of the centre. This must be unique.
        :param phone: The phone number of the centre.
        :param suburb: The suburb in which the centre is located.
        :return: If successful, the Centre object, otherwise None.
        """
        # Initialise new Centre using passed arguments.
        centre = Centre(type=type, abn=abn, name=name, phone=phone, suburb=suburb)

        # Below will throw exception if name or abn is already in-use.
        try:
            # Add new centre record to Centre table.
            db.session.add(centre)
            db.session.commit()

            # Also add centre to list of centres to minimise required DB interaction.
            self._centres.append(centre)

            return centre
        except Exception as e:
            self._logger.error(str(e))

        return None

    def get_centres(self):
        """
        Public accessor to get get all user records.

        :return: A list of User records.
        """
        return self._centres
