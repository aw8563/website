README.md
=========

Requirements
------------

You'll need to have Python 3 and virtualenv installed. It's also highly recommended that you [install virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html), which will make your life a lot easier. I will be using virtualenv wrapper commands in my installation & run instructions.
You don't NEED to have virtualenvwrapper - if you want to climb to High Hrothgar without fast travel, feel free.

Installation & Running
----------------------

Prior to running this application, you'll need to do a couple things:

	1). Create or activate a virtualenv (using python3)

		Create a virtualenv:
		mkproject -p `which python3` 1531  

		Activate a virtualenv
		workon 1531

		---

		OR

		virtualenv --python=python3 venv
		. venv/bin/activate
		
	2). Install pip dependencies
	
		pip install -r requirements.txt
		
	3). Create database, perform migrations, upgrade, then add CSV data

	    flask init_db

	4). You're good to go, run flask
	   
	   flask run

		If you get errors, you may need to set some environment variables prior to running:
			export FLASK_APP=run.py
			export FLASK_ENV=development
			export FLASK_DEBUG=1
			
			flask run
			

Login details are in app/static/data
Provider.csv, Patients.csv and Specialist.csv

Tada!

If you get operational errors on when trying to migrate or sqlite3 cant find certain tables / columns / whatever,
run 'flask rm_db' and attempt steps 3-4 again.

