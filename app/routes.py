# routes.py
#
# This file defines the different URLs (routes) our webserver implements.
# Handlers for each of these routes, known as views, are also defined here.
#
# Yeahhh boiiii - das my guy - Clancy Rye

import csv
import datetime
import os

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import app
from app.appointment import *
from app.centre import *
from app.forms import LoginForm, RegistrationForm
from app.health_care_system import HealthCareSystem
from app.user import *

import sys

# Dirty hack - basically makes sure we don't try to use the database unless we're sure it's ready.
# Otherwise Flask will try to use the database - even if we are using 'flask init_db' or 'flask rm_db'
if sys.argv[1] == 'run':
    hsc = HealthCareSystem()

# This contains temp info from .csv files
centre_list = []
provider_list = []
user1 = Patient(full_name="andy", email_address="andy@gmail.com")
user2 = Patient(full_name="james", email_address="james@gmail.com")
user3 = HealthCareProvider(full_name="jessica", email_address="jessica@gmail.com", is_provider=1)

curr_user = user1

with open('app/static/data/health_centres.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        centre_type = row['centre_type']
        centre_name = row['name']
        centre_phone = row['phone']
        centre_id = row['abn']
        centre_sub = row['suburb']
        centre = HealthCareCentre(centre_name, centre_sub, centre_phone, type=centre_type)
        centre_list.append(centre)

with open('app/static/data/provider.csv') as g:
    reader = csv.DictReader(g)
    for row in reader:
        email = row['provider_email']
        type = row['provider_type']
        pw = row['password']
        provider = HealthCareProvider(email_address=email, type=type)
        provider_list.append(provider)

with open('app/static/data/provider_health_centre.csv') as g:
    reader = csv.DictReader(g)
    n = 0
    for row in reader:
        email = row['provider_email']
        centre = row['health_centre_name']
        # assign the class centre rather than the string
        for c in centre_list:
            if centre == c._name:
                centre_class = c
        # similarly assign the class provider rather than the email
        for p in provider_list:
            if email == p._email_address:
                provider_class = p

        for provider in provider_list:
            if provider._email_address == email:
                provider.add_centre(centre_class)  # add centre to provider

        for c in centre_list:  # add provider to centre
            if (c._name == centre):
                c.add_provider(provider_class)
                # c.addProvider(email[0:email.find('@')])


@app.route('/')
@login_required
def index():
    """
    This view represents the handler for the root 'index' or 'home' screen of
    the application.

    This is loaded when no route is specified in the URL, or when redirected to
    as a 'safety net'.
    """

    return render_template('index.html', title='home', user=curr_user)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    done_booking = 0
    now = str(datetime.datetime.now())
    date = now[0:now.find(" ")]
    time = now[now.find(" ") + 1:now.find(".") - 3]
    app = ""
    if request.method == "POST":
        book = int(request.form["book"])
        # parameters for search
        c = request.form["c"]  # search for centres
        p = request.form["p"]  # search for providers
        search = request.form["search"]  # search input
        provider = request.form['provider']  # provider currently being booked for

        for prov in provider_list:
            if prov._full_name == provider:
                provider_class = prov  # returns the instance of provider

        if (book):  # if we are booking

            # set date/time/centre

            date = request.form["date"]
            centre = request.form["centre"]
            time = str(request.form["time"])
            length = int(request.form["length"])

            # convert time to minutes then add on the legnth of appointment and convert back to time
            total_len = time_to_min(time) + length
            time_end = min_to_time(total_len)

            print("curent appointment starts:" + time + " ends:" + time_end)
            # checking the times and dates are valid
            for app in provider_class._appointment_list:
                clash = time_clash(time, app._start_time, time_end, app._end_time)
                if (clash):
                    return render_template('booking.html', user=curr_user, c=c, p=p, search=search, \
                                           provider=provider_class, book=-1, t=time, d=date, app=app)

            if (date == ""):  # just for testing, this should never happen
                return render_template('booking.html', user=curr_user, c=c, p=p, search=search, provider=provider_class,
                                       noDate=1)

            app = Appointment(start_time=time, end_time=time_end, date=date, patient=curr_user,
                              health_care_provider=provider_class, centre=centre)
            done_booking = 1

    return render_template('booking.html', user=curr_user, c=c, p=p, search=search, provider=provider_class,
                           book=done_booking, t=time, d=date, app=app)


@app.route('/profile/<c>', methods=['POST', 'GET'])
def profile(c):
    print("HEREHREHREHRHERHEH")
    if (request.method == "POST"):
        c = request.form["c"]
        p = request.form["p"]
        search = request.form["search"]
        text = request.form['provider']

        for a in provider_list:
            if (a._email_address == text):
                return render_template('profile.html', object=a, c=c, p=p, search=search)

        print("search is " + search)
        for centre in centre_list:
            if (text == centre._name):
                return render_template('profile.html', object=centre, c=c, p=p, search=search)

        apple = HealthCareCentre("asdf", "asdf")
        return render_template('profile.html', object=apple, c=c, p=p, search=search)


@app.route('/search', methods=['GET', 'POST'])
def search():
    print("DSJKFLKJLDSF")
    if (request.method == 'POST'):  # redirect to the search screen
        search = request.form['search']
        search_c = int(request.form['c'])
        search_p = int(request.form['p'])
        results = []  # for centres
        results2 = []  # for providers

        if (search == ""):
            return render_template('search.html', empty=1, c=search_c, p=search_p)

        for centres in centre_list:
            # if (matchC(centres, search)):
            if (centres.match_centre(search)):
                results.append(centres)
                for p in centres._provider_list:
                    results2.append(p)

        for providers in provider_list:
            # if (matchP(providers, search)):
            if (providers.match_provider(search)):
                results2.append(providers)
                for c in providers._working_centre:
                    results.append(c)

        results = list(set(results))
        results2 = list(set(results2))

        if (not search_c):
            results = []
        if (not search_p):
            results2 = []
        if (len(results) > 0 or len(results2) > 0):
            return render_template('search.html', display=results, display2=results2, s=search, c=search_c, p=search_p,
                                   results=1)

        else:
            return render_template('search.html', s=search, results=1, noDisplay=1, c=search_c, p=search_p)

    return render_template('search.html', title='search', c=1, p=1)


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
        # If entered details have passed validation, create the new user and add them to our user table.
        # -- TODO: We're assuming user is a patient, should update form to allow for role and workplace.
        hsc.user_manager.add_user(form.username.data, form.email.data, form.password.data, role='Patient')

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

        # If credz pass validation, attempt to log the user in using them.
        if hsc.user_manager.login_user(form.username.data, form.password.data):
            # If we've arrived here, their credz are correct and they have been authenticated, redirect to the index.
            return redirect(url_for('index'))

        else:
            # User has failed to log in, display an error and redirect to the login screen.
            flash('Error: Provided username or password is incorrect.')
            return redirect(url_for('login'))

    # Render the login screen.
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    This view simply logs out the user, if they're logged in. (By terminating
    their current session).

    If the user is not logged in, this method does nothing.
    """

    hsc.user_manager.logout_user()
    return redirect(url_for('index'))


@app.route('/appointments')
def appointments():
    return render_template('appointments.html')


@app.route('/currBooking', methods=["GET", "POST"])
def curr_booking():
    cancel = 0
    if (request.method == 'POST'):
        view = int(request.form['view'])
        if (view):
            c = request.form['c']
            p = request.form['p']
            s = request.form['search']
            result = request.form['result']
            provider = request.form['provider']

            return render_template('currBooking.html', user=curr_user, cancel=cancel, l=len(curr_user._appointment_list),
                                   view=view, c=c, p=p, search=s, result=result, provider=provider)

        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        centre = request.form['centre']
        print(name + time + date + centre)
        for a in curr_user._appointment_list:
            if (
                                    time == a._start_time and date == a._date and centre == a._centre and name == a._health_care_provider._full_name):
                curr_user.remove_appointment(a)
                cancel = 1
                # curr_user.removeAppointment(app)
    length = len(curr_user._appointment_list)
    return render_template('currBooking.html', user=curr_user, cancel=cancel, l=length)
