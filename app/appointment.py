class Appointment:
    """docstring for appointment"""

    def __init__(self, start_time="", end_time="", date="", patient="", health_care_provider="", fee="", centre=""):
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

    def remove_appointment(self):
        self.get_patient().remove_appointment(self)
        self.get_health_care_provider().remove_appointment(self)

    def __str__(self):
        return self


# converts given time format to minutes
def time_to_min(time):
    minutes = int(time[-2:])
    hours = int(time[:-3])
    return int(hours * 60 + minutes)


# converts given minutes into 24hr time format
def min_to_time(num):
    minutes = num % 60
    hours = int((num - minutes) / 60)

    return str(hours) + ":0" + str(minutes) if minutes <= 9 else str(hours) + ":" + str(minutes);


# returns True if there is a clash between time1 range and time2 range
def time_clash(start1, start2, end1, end2):
    start1 = time_to_min(start1)
    start2 = time_to_min(start2)
    end1 = time_to_min(end1)
    end2 = time_to_min(end2)

    if (end1 >= start2 and start1 <= end2 or \
                        end2 >= start1 and start2 <= end1 or \
                        start1 <= start2 and end2 <= end1 or \
                        start2 <= start1 and end1 <= end2):
        return True

    return False
