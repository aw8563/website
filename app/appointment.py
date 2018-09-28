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
    def __str__(self):
        return self
