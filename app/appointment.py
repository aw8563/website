class appointment:
    """docstring for appointment"""
    def __init__(self, start_time = "", end_time = "", date = "", patient = "", health_care_provider = "", fee = "", centre = ""):
        self._start_time = start_time
        self._end_time = end_time
        self._date = date
        self._patient = patient
        self._health_care_provider = health_care_provider
        self._fee = fee
        self._centre = centre
        patient.add_appointment(self)
        health_care_provider.add_appointment(self)

    def get_start_time(self):
        return self._start_time
    def get_end_time(self):
        return self._end_time
    def get_date(self):
        return self._date
    def get_patient(self):
        return self._patient
    def get_health_care_provider(self):
        return self._health_care_provider
    def get_fee(self):
        return self._fee
    def get_centre(self):
        return self._centre


    def set_start_time(self, new_start_time):
        self._start_time = new_start_time
    def set_end_time(self, new_end_time):
        self._end_time = new_end_time
    def set_date(self, new_date):
        self._date = new_date
    def set_patient(self, new_patient):
        self._patient = new_patient
    def set_health_care_provider(self, new_health_care_provider):
        self._health_care_provider = new_health_care_provider
    def set_fee(self, new_fee):
        self._fee = new_fee
    def set_centre(self, new_centre):
        self._centre = new_centre

    def removeAppointment(self):
        self.get_patient().removeAppointment(self)
        self.get_health_care_provider().removeAppointment(self)

    def __str__(self):
        return self
