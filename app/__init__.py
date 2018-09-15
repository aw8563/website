# app/__init__.py
#
# This file is called when importing 'app', it acts as a bootstrap script to
# initialise and configure important parts of our Flask web application.
#
# Currently, this file has three responsibilities:
#     1). Instantiate and configure the Flask application.
#     2). Instantiate and configure the login manager.
#     3). Instantiate and configure our database interfaces.
#
# You can read more about Flask here: http://flask.pocoo.org/

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialise the Flask application using settings in app/config.py
app = Flask(__name__)
app.config.from_object('app.config')

# Initialise login manager and set view handling logins to our 'login' view.
login = LoginManager(app)
login.login_view = 'login'

# Initialise our SQL toolkit and ORM so we can interface easily with our db.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Finally, we're ready to load our views and models.
from app import routes, models
