# user_manager.py
#
# This file is responsible for user management and interacting with users.

import logging

from flask_login import login_user, logout_user
from termcolor import colored

from app import db
from app.models import User


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

    def works_at(self, username):
        """

        :param username: Given a username, returns a list of all the places they work.
        :return: A list of all the places a user works. If they work at none, return an empty list.
        """

        # If exists, get the user specified by username
        user = self._users.filter_by(username=username)
        if user:
            print(str(user.centres))
            return user.centres

        # print(self._users.filter_by())

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

    def get_user(self, username):
        """
        Given a username, attempts to return a User object with that username.
        :param username: The username of the user to fetch.
        :return: The user with the specified username, if they exist. Otherwise, None.
        """

        return User.query.filter_by(username=username).first()

    def get_users(self):
        """
        Returns a list of all User records.

        :return: A list of User records.
        """

        return self._users

    def login_user(self, username, password, remember=True):
        """
        Given a username and password, attempts to log a user in. If successful, logs in the user and returns true.
        Otherwise, returns False

        :param username: The username to attempt to log in with.
        :param password: The password to attempt to log in with.
        :param remember: User's "remember me" preference. Defaults to True.
        :return: True, if login was completed successfully, False otherwise.
        """

        # If the user doesn't exist, or the password is incorrect, fail the login.
        user = self.get_user(username)
        if user is None or not user.check_password(password):
            self._logger.warn("Login attempt for '%s' failed." % username)
            return False
        else:
            login_user(user, remember=remember)
            self._logger.info("Login attempt for '%s' succeeded." % username)
            return True

    def logout_user(self):
        """
        Logs out the user calling this function. If the user is not logged in, this method does nothing.

        :return: None
        """

        logout_user()
