# config.py
#
# Application-specific configuration values are stored here.
# For more information, see http://flask.pocoo.org/docs/1.0/config/

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#--------------------------------------------------------------------#
#                       FLASK ENVIRONMENT VARS                       #
#--------------------------------------------------------------------#
SECRET_KEY = os.environ.get('SECRET_KEY') or 'Dummy_Key_Woo'

#--------------------------------------------------------------------#
#                          SQLALCHEMY VARS                           #
#--------------------------------------------------------------------#
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
