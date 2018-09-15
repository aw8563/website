# run.py
#
# This file is our entrypoint for the web application. Its main responsibility
# is as a bootstrap script to instantiate and configure our Flask web app.
#
# It has a secondary function of configuring our Flask shell so we're able to
# use the 'flask shell' command to easily have access to our database and user
# contexts.
#
# The method this file uses to instantiate and configure our Flask web app is a
# little hidden - it achieves this by importing app, which loads
# app/__init__.py, which contains the actual instantiation and configuration.
# :)


#--------------------------------------------------------------------#
#                        HEY - STOP RIGHT NOW                        #
#--------------------------------------------------------------------#

# Don't call this script directly. Instead, use 'flask run'.

from app import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
