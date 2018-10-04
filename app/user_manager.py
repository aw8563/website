# user_manager.py
#
# This file is responsible for user management and interacting with users.

import logging

from app import db
from app.models import User

from termcolor import colored


class UserManager:
    """
    Class which is responsible for user management for the Medi-soft HCS. Namely, it provides abstraction for:
        - User creation.
        - User deletion.
        - User authentication, authorisation & session management.

    Largely, it does this by querying the Medi-soft Sqlite3 backend and maintaining a queriable list of records.
    """

    def __init__(self):
        """
        Constructor for UserManager class.

        Initialises a list of users from all existing User records.
        """

        # Initialise UserManager attributes.
        self._logger = logging.getLogger(__name__)

        # Load all existing users from database.
        self._users = self._load_users()

        # Indicate successful creation of HCS.
        self._logger.debug(colored("Initialised new UserManager.", 'yellow'))

    def _load_users(self):
        """
        Queries the database and returns all user records as a list. Used to initialise the class upon creation.

        :return: A list of records for each user.
        """
        self._logger.info(colored('Loading existing users.', 'yellow'))
        users = User.query.all()
        self._logger.info(colored('Loaded users: %s' % users, 'green'))

        return users

    def add_user(self, username, email, password, role='Patient'):
        """
        Creates a new user and adds it to the user database. If successful, also appends new user to current users list.

        :param username: The username of the user to add.
        :param email: The email of the user to add.
        :param role: The role of the user. (GP, patient, etc).
        :param password: The password of the user to add.
        :return: If successful, the user object, otherwise None.
        """

        # Initialise new user - always remember to season your passwords to taste.
        user = User(username=username, email=email, role=role)
        user.set_password(password)

        # Below will throw exception if email is already registered.
        try:
            # Add new user record to User table.
            db.session.add(user)
            db.session.commit()

            # Also add user to list of users to minimise required DB interaction.
            self._users.append(user)

            return user
        except Exception as e:
            self._logger.error(str(e))

        return None

    def get_users(self):
        """
        Public accessor to get get all user records.

        :return: A list of User records.
        """
        return self._users
