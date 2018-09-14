README.md
=========

Requirements
------------

You'll need to have Python 3 and virtualenv installed. It's also highly recommended that you [install virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html), which will make your life a lot easier. I will be using virtualenv wrapper commands in my installation & run instructions.

Installation & Running
----------------------

Prior to running this application, you'll need to do a couple things:

	1). Create or activate a virtualenv (using python3)

		Create a virtualenv:
		mkproject -p `which python3` 1531  

		Activate a virtualenv
		workon 1531

	2). Install pip dependencies
	
		pip install -r requirements.txt
		
	3). Create database and perform migrations
	
	   flask db init
	   flask db migrate
	   flask db upgrade
	   
	4). You're good to go, run flask
	   
	   flask run

		If you get errors, you may need to set some environment variables prior to running:
			export FLASK_APP=run.py
			export FLASK_ENV=development
			export FLASK_DEBUG=1
			
			flask run
			
Tada!

If you get operational errors on when trying to migrate or sqlite3 cant find
certain tables / columns / whatever, try deleting your migrations folder and
app.db and peforming step 3 again. <3

