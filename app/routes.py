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
from app.searchParam import *

#This contains temp info from .csv files

centreList = []
providerList = []
patientList = []
user1 = patient(full_name = "andy", email_address = "andy@gmail.com")
user2 = patient(full_name = "james", email_address = "james@gmail.com")
user3 = health_care_provider(full_name = "jessica", email_address = "jessica@gmail.com", isprovider = 1)

currUser = user3


#reading in values from csv files
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

with open('app/static/data/patient.csv') as g:
    reader = csv.DictReader(g)
    for row in reader:
        email = row['patient_email']
        pw = row['password']  
        cpatient = patient(full_name = email, email_address = email)
        patientList.append(cpatient)  


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

@app.route('/search2', methods = ["POST", "GET"])
def search2():
    if (request.method == "POST"):

        
        redir = request.form['redir'] # if the search page is redirected from anotehr page
        search = request.form['search'] # search parameters

        if (int(redir) == 0): # if not redirected from a 'return to search' 

            # get values and make the class
            suburb = request.form["suburb"]
            providerName = request.form["providerName"]
            providerType = request.form["providerType"]
            centreType = request.form["centreType"]
            centreName = (request.form["centreName"])
            viewCentre = request.form["viewCentre"]
            viewProvider = request.form["viewProvider"]
    
            search = SearchParam(centreName, providerName, suburb, centreType, providerType, \
                                 int(viewProvider), int(viewCentre))
           
        else: # if it is redirected from 'return to search' then use the old parameters
            search = makeSearchObject(search)

        results = search.results(centreList, providerList) # get search results

        c = False
        p = False

        if (search._view_centre): 
            c = True
            print(search._view_centre)
        if (search._view_provider):

            print(search._view_provider)
            p = True

        if (not c and not p):
            # if no selected display return error
            return render_template('search2.html', search = search, noView = 1, redir = 0)

        if (search._suburb == "" and search._provider_name == "" and \
            search._provider_type == "" and search._centre_type == "" \
            and search._centre_name == ""):
            # if no searh criterias return error
            return render_template('search2.html', search = search, empty = 1, redir = 0)

        # if there are no results
        if (len(results[0]) == 0 and len(results[1]) == 0):
            return render_template('search2.html', redir = 0, search = search, \
                                    results = 1, noDisplay = 1)
        
        # return results page
        return render_template('search2.html', results = 1, search = search, redir = 0, \
                               display = results[0], display2 = results[1], \
                               viewCentre = c, nCentre = len(results[0]),\
                               viewProvider = p, nProvider = len(results[1]))

    return render_template('search2.html', viewCentre = 1, viewProvider = 1, redir = 0, search = 0)


@app.route('/booking', methods = ['GET', 'POST'])
def booking():
    doneBooking = 0 
    now = str(datetime.datetime.now())
    date = now[0:now.find(" ")]
    time = now [now.find(" ") + 1:now.find(".") - 3]
    app = ""
    if (request.method == "POST"):
        book = int(request.form["book"]) # if we are making a booking
        search = request.form["search"] # current search parameters
        provider = request.form['provider'] # provider currently being booked for

        for prov in providerList:
            if (prov._full_name == provider):
                providerClass = prov # returns the instance of provider

        if (book): # if we are booking

            # set date/time/centre
            date = request.form["date"]
            centre = request.form["centre"]
            time = str(request.form["time"])
            length = int(request.form["length"])
        
            # convert time to minutes then add on the legnth of appointment
            # and convert back to 24hr time format
            totalLen = timeToMin(time) + length       
            timeEnd = minToTime(totalLen)

            # checking the times and dates are valid
            for app in providerClass._appointment_list:
                clash = timeClash(time, app._start_time, timeEnd, app._end_time)
                if (clash): # if htere is clash return error
                    return render_template('booking.html', user = currUser, search = search, \
                           provider = providerClass, book = -1, t = time, d = date, app = app)

            for app in currUser._appointment_list:
                clash = timeClash(time, app._start_time, timeEnd, app._end_time)
                if (clash): # if htere is clash return error
                    return render_template('booking.html', user = currUser, search = search, \
                           provider = providerClass, book = -1, t = time, d = date, app = app)

                
            if (date == ""):  #just for testing, this should never happen
                return render_template('booking.html', user = currUser, search = search, \
                                        provider = providerClass, noDate = 1)
            
            # make booking if it passes checks
            app = appointment(start_time = time,end_time = timeEnd, date = date, patient = \
                              currUser,health_care_provider = providerClass, centre = centre)
            doneBooking = 1

    return render_template('booking.html', user = currUser, search = search, provider = \
                           providerClass, book = doneBooking, t = time, d = date, app = app)


# profile page
@app.route('/profile/<c>', methods = ['POST', 'GET'])
def profile(c):
    if (request.method == "POST"):
        
        israting = int(request.form["israting"]) # if we are makign a rating      
        search = makeSearchObject(request.form["search"]) # current search parameters      
        text = request.form['provider'] # email of te provider/centre
        
        for a in providerList: # check if it's a provider
            if (a._email_address == text):
                if israting: # if we are rating 
                    rating = int(request.form["rating"])
                    a.add_rating(rating)
                return render_template('profile.html', object = a, search = search)
        
        for centre in centreList: # check for which centre if it is not a provider
            if (text == centre._name):
                if israting: # if we are rating 
                    rating = int(request.form["rating"])
                    centre.add_rating(rating)

                return render_template('profile.html', object = centre, search = search)

        # deugging. This part should never happen
        apple = health_care_centre("asdf","asdf")
        return render_template('profile.html', object = apple, c = c, p = p, search = search)

# old search.
@app.route('/search', methods = ['GET', 'POST'])
def search():
    
    
    if (request.method == 'POST'): #redirect to the search screen
        search = request.form['search']
        searchC= int(request.form['c'])
        searchP = int(request.form['p'])
        results = [] #for centres
        results2 = [] #for providers

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

@app.route('/myProfile')
def myProfile():
    #print(current_user)
    #andy = patient("ANDY WANG", "andy@gmail.com", 000, 111)
    #james = health_care_provider("JAMES FENG", "james@gmail.com", 222, 333)
    #print(andy)
    #currentuser = patientList[0]
    #print(currentuser)
    return render_template('myProfile.html', object = currUser)

@app.route('/updateInfo', methods = ['GET', 'POST'])
def updateInfo():
    #currentuser = patientList[0]
    """
    if (request.method == "POST"):
        useremail = request.form['useremail']
        #updating = int(request.form['updating'])
        for user in patientList: 
            if (user._email_address == useremail):
                return render_template('updateInfo.html', object = user)
        return  render_template('updateInfo.html', object = andy)
    """
    if (request.method == "POST"):
        if (isinstance(currUser, patient) == True):
            newName = request.form['newName']
            newEmail = request.form['newEmail']
            newPhone = request.form['newPhone']
            newMedicare = request.form['newMedicare']
            print(newName + newEmail + newPhone + newMedicare)
            currUser.changeDetails(newName, newEmail, newPhone, newMedicare)
            print(currUser)

        else:
            newName = request.form['newName']
            newEmail = request.form['newEmail']
            newPhone = request.form['newPhone']
            newProvider = request.form['newProvider']
            newType = request.form['newType']
            currUser.changeDetails(newName, newEmail, newPhone, newProvider, newType)

        return render_template('updateInfo.html', object = currUser)

    return render_template('updateInfo.html', object = currUser)

    
# view bookings 
@app.route('/currentBookings', methods = ["GET", "POST"])
def currentBookings():

    remove = 0 #remove a single booking
    removeAll = 0 # remove all bookings
    fromBooking = 0 # redirected from booking page
    provider = ""
    search = ""

    if request.method == "POST":

        fromBooking = int(request.form['fromBooking']) #redirected from booking page
        if (fromBooking): #get provider and sesarch paramters
            provider = request.form['provider']
            search = request.form['search']

        remove = int(request.form['remove']) # if we are cancelling a booking

        if (remove == 1):
            
            # get appointment info
            name = request.form['name']
            time = request.form['time']
            date = request.form['date']
            centre = request.form['centre']


            # find the instance of that appointment and remove it form user and provider
            for a in currUser._appointment_list:
                if (time == a._start_time and date == a._date and centre == a._centre\
                    and name == a._health_care_provider._full_name):
                    print("HERE")
                    a.removeAppointment()


        if (remove == 2): # remove all    
            for a in currUser._appointment_list:
                a._health_care_provider.removeAppointment(a)
                
            currUser._appointment_list = []
            currUser._numAppointments = 0  

    return render_template('currentBookings.html', user = currUser, removeAll = removeAll, \
                            remove = remove, l = len(currUser._appointment_list), \
                            provider = provider, search = search, fromBooking = fromBooking)

