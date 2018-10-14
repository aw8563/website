# routes.py
#
# This file defines the different URLs (routes) our webserver implements.
# Handlers for each of these routes, known as views, are also defined here.
#
# Yeahhh boiiii - das my guy - Clancy Rye

import logging
import sys
from datetime import datetime, timedelta
import operator


from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from termcolor import colored

from app import app
from app import db
from app.centre_manager import CentreManager
from app.forms import LoginForm, RegistrationForm
from app.health_care_system import HealthCareSystem
from app.models import Centre, User, Appointment, WorksAt
from app.user_manager import UserManager
from app.models import *

logger = logging.getLogger(__name__)

# Dirty hack - basically makes sure we don't try to use the database unless we're sure it's ready.
# Otherwise Flask will try to use the database - even if we are using 'flask init_db' or 'flask rm_db'
if sys.argv[1] == 'run':
    hsc = HealthCareSystem()


# ----- Public pages ----- #
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


# ----- Private pages ----- #


@app.route('/')
@login_required
def index():
    """
    This view represents the handler for the root 'index' or 'home' screen of
    the application.

    This is loaded when no route is specified in the URL, or when redirected to
    as a 'safety net'.
    """

    return render_template('index.html', title='home')


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    """
    Create a new booking with a provider.

    :return:
        GET: Creates and renders a page which can be used to create a booking for a provider.
        POST: Creates a booking using information from the provided posted form.
    """

    # Initialise provider and result to None so we don't get undefined errors
    provider = None
    result = None

    logger.info(colored(request.form, "yellow"))

    # If we're fielding a post request, we're stepping through the booking process
    if request.method == 'POST':
        
        # If we've got a provider previously selected (from either search or previous step)
        provider_selection = request.form.get('provider_selection', None)
        if provider_selection:

            # Fetch it, as we need to reference provider attributes
            provider = UserManager.get_user(provider_selection)
            logger.info(colored(provider.username, "yellow"))

            # Attempt to fetch the date and time from the form
            date = request.form.get('date', False)
            time = request.form.get('time', False)

            # If we've got them, try to book the appointment, otherwise the user hasn't selected them yet.
            if date and time:

                # Parse date and determine end_time as 30 minutes after the starting time.
                start_time = datetime.strptime(date + "_" + time, '%d/%m/%Y_%H:%M')
                end_time = start_time + timedelta(minutes=30)

                centre = request.form.get('centre_selection')
                result = WorksAt.are_valid_hours(start_time, end_time, centre, provider.email)

                # If result is empty, no error was encountered - we're good to go, create and add the appointment.
                if not result:

                    # We might want to abstract this, but I'm not too sure tbh.
                    a = Appointment(patient_email=current_user.email, provider_email=provider.email, centre_name=centre,
                                    is_confirmed=0, start_time=start_time, end_time=end_time, reason=request.form.get('reason'))

                    db.session.add(a)
                    db.session.commit()

                    result = "Added"
                    logger.info(colored("Added appointment", 'green'))
            logger.warn(colored(request.form, 'green'))

    # Get all providers so we can choose from them
    providers = User.query.filter(User.role.isnot('Patient')).all()
    return render_template('booking.html', title="Make a booking", result=result, provider=provider, providers=providers)


@app.route('/profile/<name>', methods=['POST', 'GET'])
@login_required
def profile(name):
    """
    Endpoint that handles User and Centre profiles.

    :param name: The user or centre name whose profile we're viewing.
    :return:
      GET:  Creates and renders a profile page for a Centre or User.
      POST: ???
    """
    
    # Determine what kind of profile we should be rendering
    profile_type = hsc.determine_type(name)

    ratingType = "centre"
    providerEmail = ""
    centreName = ""
    rated = False

    if profile_type == 'user':
        obj = UserManager.get_user(name)
        providerEmail = obj.email
        ratingType = "provider"
    elif profile_type == 'centre':
        obj = CentreManager.get_centre(name)
        centreName = obj.name
    else:
        return 'Something went wrong, undetermined type for "%s"' % name

    if (request.method == "POST"):
        score = int(request.form["rating"])
        rating = Rating(type = ratingType, rating = score, patient_email = current_user.email,\
                        provider_email = providerEmail, centre_name = centreName)       
        
        db.session.add(rating)
        db.session.commit()
        rated = True

    
    logger.warn(colored(name, "red"))
    logger.warn(colored(obj, "red"))



    # Can the current user view the patient's history?
    permission = False
    if (current_user.role != 'patient' and profile_type == 'user'): 
        # make sure current user is a provider
        for b in current_user.patient_bookings: # and also booked with the patient  
            if (b.patient_email == obj.email):
                permission = True
               
    print(permission) 
    return render_template('profile.html', object=obj, type=profile_type, rated = rated,\
                            permission = permission, user = current_user)
   


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    Endpoint that handles user searches. Given specific search criteria, queries the Medi-soft database then displays
    the results to the user.

    :return:
        GET:  Creates and renders the search page, along with search forms used to submit a search.
        POST: Submits search query and returns renders results.
    """

    logger.info(colored(request.form, "red"))
    results_found = False

    # If user is submitting a search, perform the search and display results
    if request.method == 'POST':
        # Initialise results to be None so we don't error on return.
        centre_results = user_results = []

        # Fetch the search query and search options, defaulting to False if non-existent.
        do_centre_search = request.form.get('do_centre_search', False)
        do_user_search = request.form.get('do_user_search', False)

        # # If we're performing a Centre search, fetch appropriate variables.
        if do_centre_search:
            name = request.form['c_name']
            type = request.form['c_type']
            suburb = request.form['c_suburb']
            centre_results = Centre.do_search(name, type, suburb)

            logger.info(colored("Centre results:", "red"))
            logger.info(colored(centre_results, "red"))

        # If we're performing a Provider search, fetch appropriate variables.
        if do_user_search:
            name = request.form['u_name']
            type = request.form['u_type']
            user_results = User.do_search(name, type)

            logger.info(colored("User results:", "red"))
            logger.info(colored(user_results, "red"))

        # If there are any results, set results_found to True, otherwise set it to False.
        if len(centre_results) > 0 or len(user_results) > 0:
            results_found = True
        else:
            results_found = False

        return render_template('search.html', form=request.form, results_found=results_found,
                               centre_results=centre_results, user_results=user_results)

    return render_template('search.html', form=None, results_found=results_found, display_results=False)

@login_required
@app.route('/appointmentDetails/<ID>', methods=["GET", "POST"])
def appointmentDetails(ID):
    
    app = Appointment.query.filter_by(id = ID).first()
    
    return render_template('appointmentDetails.html', app = app)

@login_required
@app.route('/modifyNote/<ID>', methods=["GET", "POST"])
def modifyNote(ID):
    app = Appointment.query.filter_by(id = ID).first()
    change = False
    patient = app.patient.email
    if (request.method == "POST"):
        action = request.form['action']
        if (action == 'edit'):
            app.notes = request.form['message']
            db.session.commit()
            change = True
        if (action == 'add'):
            app.notes += " " + request.form['message']
            db.session.commit()
            change = True
            
    return render_template('modifyNote.html', app = app, patient = patient, \
                                              user = current_user, change = change)

@app.route('/manage_bookings', methods=["GET", "POST"])
@login_required
def manage_bookings():
    """
    Enables the user to view their current bookings / appointments.

    :return:
        GET:  Creates and renders the booking page, along with forms used to book an appointment.
        POST: Deletes an existing booking
    """
    
    # User is deleting booking
    if request.method == 'POST':
        logger.debug(colored(request.form, 'yellow'))

        if request.form["action"] == 'complete': #confirm the booking request
            appID = request.form['id']
            a = Appointment.query.filter_by(id = appID).first()
            a.is_completed = True
            db.session.commit()

        if request.form["action"] == 'confirm': #confirm the booking request
            appID = request.form['id']
            a = Appointment.query.filter_by(id = appID).first()
            a.is_confirmed = True
            db.session.commit()

        if request.form.get("action", False) == 'cancel':
            Appointment.delete_appointment(request.form.get("appointment_id", False))

    pendingBookings = []
    confirmedBookings = []
    completedBookings = []

    if (current_user.role == 'Patient'): #sort patient bookings with a provider
        for b in current_user.provider_bookings:
            if b.is_completed:
                completedBookings.append(b)
            elif b.is_confirmed:
                confirmedBookings.append(b)
            else:
                pendingBookings.append(b)
    else: #sort bookings that a provider has with patient
        for b in current_user.patient_bookings:
            if b.is_completed:
                completedBookings.append(b)
            elif b.is_confirmed:
                confirmedBookings.append(b)
            else:
                pendingBookings.append(b)

    # sort into chronological order
    pendingBookings.sort(key=operator.attrgetter('start_time'))
    confirmedBookings.sort(key=operator.attrgetter('start_time'))
    completedBookings.sort(key=operator.attrgetter('start_time'))

    return render_template('manage_bookings.html', user=current_user, \
                            completed = completedBookings, \
                            confirmed = confirmedBookings, \
                            pending = pendingBookings)


@login_required
@app.route('/patientHistory/<name>', methods=['GET', 'POST'])
def patientHistory(name):
    patient = UserManager.get_user(name)
    nCompleted = 0
    for b in patient.provider_bookings:
        if b.is_completed:
            nCompleted += 1
    patient.provider_bookings.sort(key=operator.attrgetter('start_time'))
    return render_template('patientHistory.html', patient = patient, len = nCompleted)

