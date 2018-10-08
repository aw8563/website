# health_care_system.py
#
# The 'main' class which is responsible for orchestrating all of the health system. Largely, it consists of:
#   - A user manager, which stores and provides an interface to users of the Medi-soft system. EG.
#       * Adding and removing users.
#       * Authenticating and managing user sessions.
#   - A list of HealthCareCentres in the Medi-soft system.

import csv
import logging
from datetime import datetime

from termcolor import colored

from app.centre_manager import CentreManager
from app.models import *
from app.user_manager import UserManager


class HealthCareSystem:
    """
    This class is used to store and interact with all the data required by the HealthCareSystem.
    Largely, it contains:
        - A list of health_care_centres.
        - A user manager, which stores and allows us to interface with user data.
    """

    def __init__(self):
        """
        Constructor for HealthCareSystem class.

        Initialises UserManager and CentreManager, which allow us to interact with our stored data.

        """
        # Initialise HCS attributes.
        self._logger = logging.getLogger(__name__)

        self.centre_manager = CentreManager()
        self.user_manager = UserManager()

        self._logger.debug("Initialised new HealthCareSystem.")

    def load_from_csv(self):
        """
        Loads the Medi-soft database with data from the provided CSV files. This method can be called by "flask init_db"

        :return: None
        """

        # Load patients from patient.csv
        self._logger.info(colored("Initialising patients", "yellow"))
        with open('app/static/data/patient.csv') as f:
            reader = csv.DictReader(f)
            for r in reader:
                self._logger.debug(str(r))
                # TODO: Do we need to handle the 'usual' format?
                self.user_manager.add_user(r['patient_email'], r['patient_email'], r['password'], r['phone_number'],
                                           r['medicare_number'])

            self._logger.info(colored("Patients initialised", "green"))

            # Load providers from provider.csv
            self._logger.info(colored("Initialising providers", "yellow"))
            with open('app/static/data/provider.csv') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self._logger.debug(str(r))
                    # TODO: Do we need to handle the 'usual' format?
                    self.user_manager.add_user(r['provider_email'], r['provider_email'], r['password'],
                                               r['phone_number'],
                                               None, r['provider_number'], role=r['provider_type'])

                self._logger.info(colored("Providers initialised", "green"))

            # Load centres from health_centres.csv
            self._logger.info(colored("Initialising centres", "yellow"))
            with open('app/static/data/health_centres.csv') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self._logger.debug(str(r))
                    self.centre_manager.add_centre(r['centre_type'], r['abn'], r['name'], r['phone'], r['suburb'])

                self._logger.info(colored("Centres initialised", "green"))

            # Load 'works at' relations from provider_health_centre.csv
            self._logger.info(colored("Initialising works_at relations", "yellow"))
            with open('app/static/data/provider_health_centre.csv') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self._logger.debug(str(r))

                    # TODO: Maybe should be part of user_manager?
                    # TODO: Do we need to handle the 'usual' format?
                    hours_start = datetime.strptime(r['hours_start'], '%H:%M:%S').time()
                    hours_end = datetime.strptime(r['hours_end'], '%H:%M:%S').time()
                    wa = WorksAt(provider=r['provider_email'], place=r['health_centre_name'], hours_start=hours_start,
                                 hours_end=hours_end)

                    db.session.add(wa)
                    db.session.commit()

                self._logger.info(colored("Works_At relations initialised", "green"))

            # Loads appointments from appointment.csv
            self._logger.info(colored("Initialising appointments", "yellow"))
            with open('app/static/data/appointment.csv') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self._logger.debug(str(r))

                    # TODO: Maybe should be part of user_manager?
                    # TODO: Do we need to handle the 'usual' format?
                    start_time = datetime.strptime(r['start_time'], '%H:%M:%S').time()
                    end_time = datetime.strptime(r['end_time'], '%H:%M:%S').time()

                    a = Appointment(patient_email=r['patient'], provider_email=r['provider'], centre_name=r['centre'],
                                    start_time=start_time, end_time=end_time, is_confirmed=int(r['is_confirmed']),
                                    notes=r['notes'])

                    db.session.add(a)
                    db.session.commit()

            # Loads ratings from rating.csv
            self._logger.info(colored("Initialising ratings", "yellow"))
            with open('app/static/data/rating.csv') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self._logger.debug(str(r))

                    # TODO: Maybe should be part of user_manager?
                    # TODO: Do we need to handle the 'usual' format?
                    rating = Rating(type=r['type'], rating=r['rating'], patient_email=r['patient_email'],
                                    provider_email=r['provider_email'], centre_name=r['centre_name'])

                    db.session.add(rating)
                    db.session.commit()

                self._logger.info(colored("Ratings initialised", "green"))

            # Loads prescriptions from prescription.csv
            self._logger.info(colored("Initialising prescriptions", "yellow"))
            with open('app/static/data/prescription.csv') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self._logger.debug(str(r))

                    # TODO: Maybe should be part of user_manager?
                    # TODO: Do we need to handle the 'usual' format?
                    rating = Prescription(patient_email=r['patient'], provider_email=r['provider'],
                                          appointment_id=r['appointment'],
                                          medicine=r['medicine'])

                    db.session.add(rating)
                    db.session.commit()

                self._logger.info(colored("Prescriptions initialised", "green"))
