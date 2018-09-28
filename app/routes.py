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

from app.user import *
from app.appointment import *
from app.centre import *
import csv
import datetime

#This contains temp info from .csv files
centreList = []
providerList = []
user1 = patient(full_name = "andy", email_address = "andy@gmail.com")
user2 = patient(full_name = "james", email_address = "james@gmail.com")
user3 = health_care_provider(full_name = "jessica", email_address = "jessica@gmail.com", isprovider = 1)


currUser = user1

if (1):
    with open('app/static/data/health_centres.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            centreType = row['centre_type']
            centreName = row['name'] 
            centrePhone = row['phone']
            centreID = row['abn'] 
            centreSub = row['suburb']
            centre = health_care_centre(centreName, centreSub, centrePhone, type = centreType)
            centreList.append(centre)
            

    with open('app/static/data/provider.csv') as g:
        reader = csv.DictReader(g)
        for row in reader:
            email = row['provider_email']
            type = row['provider_type']
            pw = row['password']  
            provider = health_care_provider(email_address = email,type = type)
            providerList.append(provider)  

    with open('app/static/data/provider_health_centre.csv') as g:
        reader = csv.DictReader(g)
        n = 0
        for row in reader:
            email = row['provider_email']
            centre = row['health_centre_name']
            #assign the class centre rather than the string
            for c in centreList:
                if (centre == c._name): 
                    centreClass = c
            #similarly assign the class provider rather than the email
            for p in providerList:
                if (email == p._email_address):
                    providerClass = p

            for provider in providerList:    
                if (provider._email_address == email):
                    provider.addCentre(centreClass)     #add centre to provider

            for c in centreList: # add provider to centre
                if (c._name == centre):
                    c.addProvider(providerClass)
                    #c.addProvider(email[0:email.find('@')])

@app.route('/')
@login_required
def index():
    """
    This view represents the handler for the root 'index' or 'home' screen of
    the application.

    This is loaded when no route is specified in the URL, or when redirected to
    as a 'safety net'.
    """
    
    return render_template('index.html', title='home', user = currUser)


@app.route('/booking', methods = ['GET', 'POST'])
def booking():
    doneBooking = 0
    now = str(datetime.datetime.now())
    date = now[0:now.find(" ")]
    time = now [now.find(" ") + 1:now.find(".") - 3]
    app = ""
    if (request.method == "POST"):
        book = int(request.form["book"])
        c = request.form["c"]
        p = request.form["p"]
        search = request.form["search"]
        provider = request.form['provider']

        for prov in providerList:
            if (prov._full_name == provider):
                providerClass = prov

        if (book):
            date = request.form["date"]
            centre = request.form["centre"]
            time = request.form["time"]
            #print(">>>>  " + centre)


            if (date == ""):  #just for testing, this should never happen
                return render_template('booking.html', user = currUser, c = c, p = p, search = search, provider = providerClass, noDate = 1)
            
            app = appointment(start_time = time, date = date, patient = currUser,health_care_provider = providerClass, centre = centre)
            currUser.add_appointment(app)
            doneBooking = 1

    return render_template('booking.html', user = currUser, c = c, p = p, search = search, provider = providerClass, book = doneBooking, t = time, d = date, app = app)


@app.route('/profile/<c>', methods = ['POST', 'GET'])
def profile(c):

    if (request.method == "POST"):
        c = request.form["c"]
        p = request.form["p"]
        search = request.form["search"]

        text = request.form['provider']

        for a in providerList:
            if (a._email_address == text):
                print("search is: " + search)
                return render_template('profile.html', object = a, c = c, p = p, search = search)
        

        apple = health_care_provider("andy", "andy@gmail.com", 1, 1, "GP", rating = 5)
        return render_template('profile.html', object = apple, c = c, p = p, search = search)

@app.route('/search', methods = ['GET', 'POST'])
def search():

    print("DSJKFLKJLDSF")
    if (request.method == 'POST'): #redirect to the search screen
        search = request.form['search']
        searchC= int(request.form['c'])
        searchP = int(request.form['p'])
        results = [] #for centres
        results2 = [] #for providers
        print("kys: " + search)

        if (search == ""):
            return render_template('search.html', empty = 1, c = searchC, p = searchP)


        for centres in centreList:
            #if (matchC(centres, search)): 
            if (centres.matchCentre(search)):       
                results.append(centres)
                for p in centres._providerList:
                    results2.append(p)

        for providers in providerList:
            #if (matchP(providers, search)):
            if (providers.matchProvider(search)):
                results2.append(providers)
                for c in providers._working_centre:
                    results.append(c)
                    
        results = list(set(results))
        results2 = list(set(results2))


        if (not searchC):
            results = []
        if (not searchP):
            results2 = []
        if (len(results) > 0 or len(results2) > 0):
            return render_template('search.html', display = results, display2 = results2, s = search, c = searchC, p = searchP, results = 1)

        else:
            return render_template('search.html', s = search, results = 1, noDisplay = 1, c = searchC, p = searchP)
   
    return render_template('search.html', title = 'search', c = 1, p = 1)




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

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')


@app.route('/currBooking', methods = ["GET", "POST"])
def currBooking():
    cancel = 0
    if (request.method == 'POST'):
        view = int(request.form['view'])
        if (view):
            c = request.form['c']
            p = request.form['p']
            s = request.form['search']
            result = request.form['result']
            provider = request.form['provider']
        
            return render_template('currBooking.html', user = currUser, cancel = cancel, l = len(currUser._appointment_list), view = view, c = c, p = p, search = s, result = result, provider = provider)

        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        centre = request.form['centre']
        print(name + time + date + centre)
        for a in currUser._appointment_list:
            if (time == a._start_time and date == a._date and centre == a._centre and name == a._health_care_provider._full_name):
            
                currUser.removeAppointment(a)
                cancel = 1        
        #currUser.removeAppointment(app)
    length = len(currUser._appointment_list)
    return render_template('currBooking.html', user = currUser, cancel = cancel, l = length)

