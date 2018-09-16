# routes.py
#
# This file defines the different URLs (routes) our webserver implements.
# Handlers for each of these routes, known as views, are also defined here.

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse
from app.classes import *
import csv
@app.route('/')
#@login_required
def index():
    """
    This view represents the handler for the root 'index' or 'home' screen of
    the application.

    This is loaded when no route is specified in the URL, or when redirected to
    as a 'safety net'.
    """

    return render_template('index.html', title='home')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    centreList = []
    providerList = []

    with open('health_centres.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            centreType = row['centre_type']
            centreName = row['name'] 
            centrePhone = row['phone']
            centreID = row['abn'] 
            centreSub = row['suburb']
            centre = health_care_centre(centreName, centreSub, centrePhone,
                     "","", type = centreType)
            centreList.append(centre)
            

    with open('provider.csv') as g:
        reader = csv.DictReader(g)
        for row in reader:
            email = row['provider_email']
            type = row['provider_type']
            pw = row['password']  
            provider = health_care_provider(email_address = email,type = type)
            providerList.append(provider)  

    with open('provider_health_centre.csv') as g:
        reader = csv.DictReader(g)
        n = 0
        for row in reader:
            email = row['provider_email']
            centre = row['health_centre_name']
            for provider in providerList:    
                if (provider._email_address == email):
                    provider.addCentre(centre)     #add centre to provider

            for c in centreList: # add provider to centre
                if (c._name == centre):
                    c.addProvider(email[0:email.find('@')])
       
    if (request.method == 'POST'): #redirect to the search screen
        search = request.form['search']
        print(search)
        results = [] #for centres
        results2 = [] #for providers
        for centres in centreList:
            if (matchC(centres, search)):        

                results.append(centres)
                for p in centres._providerList:
                    results2.append(p)

        for providers in providerList:
            if (matchP(providers, search)):
                results2.append(providers)
                for c in providers._working_centre:
                    results.append(c)
                    
        results = list(set(results))
        results2 = list(set(results2))

        if (len(results) > 0 or len(results2) > 0):
            return render_template('results.html', display = results, display2 = results2)
   
        return render_template('results.html', display = ["EMPTY"],display2 = ["EMPTY"])

    return render_template('search.html', title = 'search')




@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This view represents the handler for our registration screen. Its behaviour
    varies depending on which HTTP verb is used with it:

        GET:  Creates and renders registration page, along with form.
        POST: Submits registration form for validation & processing.
    """

    # If the user is already logged in, get 'em outta here.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Otherwise, create a RegistrationForm for them to enter their details,
    # then validate said details after submission.
    form = RegistrationForm()
    if form.validate_on_submit():

        # If entered details have passed validation, create the new user and
        # add them to our user table.
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Woohoo, you did it! Redirecting to login screen.')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This view represents the handler for the 'login' screen. Its behaviour
    varies depending on which HTTP verb is used with it:

        GET:  Creates and renders login page, along with form.
        POST: Attempts to authenticate user with submitted login form.
    """

    # If user is already logged in, redirect them to the index page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Otherwise, create a LoginForm for them to enter their credz, then attempt
    # to authenticate them after validation.
    form = LoginForm()
    if form.validate_on_submit():

        # If entered creds pass validation, check that user exists and that
        # their password is correct.
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Error: Provided username or password is incorrect.')
            return redirect(url_for('login'))

        # If we've arrived here, their credz are correct, authenticate them,
        # then redirect back to the home page.
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """
    This view simply logs out the user, if they're logged in. (By terminating
    their current session).

    If the user is not logged in, this method does nothing.
    """

    logout_user()
    return redirect(url_for('index'))
