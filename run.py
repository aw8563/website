# run.py
#
# This file is our entry-point for the web application. Its main responsibility
# is as a bootstrap script to instantiate and configure our Flask web app.
#
# It has a secondary function of configuring our Flask shell so we're able to
# use the 'flask shell' command to easily access and interact with our database
#
# As a note - this file instantiates and configures our Flask web app by importing 'app', loading app/__init__.py,
# which contains the actual instantiation and configuration. :)

import logging
from os import remove,  makedirs
from os.path import isfile
from shutil import rmtree
from subprocess import call

from termcolor import colored

from app import app, db
from app.health_care_system import HealthCareSystem

from app.models.centre import Centre
from app.models.user import User
from app.models.works_at import WorksAt

logger = logging.getLogger(__name__)


@app.shell_context_processor
def make_shell_context():
    """
    Runs when 'flask shell' is invoked - adds database instance and models to shell session.

    :return: None
    """
    return {'db': db, 'User': User, 'WorksAt': WorksAt, 'Centre': Centre}


@app.cli.command('load_from_csv')
def load_from_csv():
    """
    Runs when 'flask load_from_csv' is invoked - enters all information from provided CSV files.

    :return: None
    """

    # We're required to do this, as UserManager is a property of HSC. A little annoying and hacky. :'(
    hsc = HealthCareSystem()
    hsc.load_from_csv()


@app.cli.command('init_db')
def init_database_command():
    """
    Runs when 'flask init_db' is invoked - prepares the database, including:
        - Initialising the database
        - Performing database migrations
        - Performing database upgrades
        - Loading CSV data into database
        - Flagging database upgrade as complete

    :return: None
    """
    logger.debug(colored("Initialising database.", "yellow"))
    call('flask db init', shell=True)

    # As we mess around with this directory, we need to ensure it exists so
    # the migration can complete successfully.
    if not isfile('./migrations/versions/'):
        call('mkdir ./migrations/versions/', shell=True)

    logger.debug(colored("Applying database migrations.", "yellow"))
    call('flask db migrate', shell=True)

    logger.debug(colored("Upgrading database.", "yellow"))
    call('flask db upgrade', shell=True)

    # logger.debug(colored("Flagging upgrades complete.", "yellow"))
    # call('touch migrations/versions/applied', shell=True)

    logger.debug(colored("Loading data from CSV files.", "yellow"))
    call('flask load_from_csv', shell=True)

    logger.debug(colored("Database initialised.", "green"))


@app.cli.command('rm_db')
def remove_database_command():
    """
    Runs when 'flask rm_db' is invoked - removes the database and migrations/versions folder.

    :return: None
    """
    logger.debug(colored("Removing database and migrations.", "yellow"))
    try:
        # Remove database and all recorded migrations before recreating empty migrations/versions folder.
        # This 'resets' the database. I selectively delete versions rather than migrations as I want to return the
        # migration logging configuration stored within migrations.
        remove('./app/app.db')
        rmtree('./migrations/versions')
        makedirs('./migrations/versions')
        logger.debug(colored("Database and migrations/versions removed.", "green"))
    except Exception as e:
        logger.error(str(e))
