from abc import ABC


class User(ABC):
    def __init__(self, full_name="", email_address="", phone_number="", password="", isprovider=0):
        name = email_address[0:email_address.find('@')]  # temp fix for no given name
        self._full_name = name
        self._email_address = email_address
        self._phone_number = phone_number
        self._password = password
        self._is_patient = 0
        self._is_provider = 0
        self._is_user = 1
        self._appointment_list = []
        self._num_appointments = 0


class Patient(User):
    def __init__(self, full_name="", email_address="", phone_number="", medicare_number="", is_provider=0):
        super().__init__(full_name, email_address, phone_number, is_provider)
        self._medicare_number = medicare_number
        self._is_patient = 1

    def get_medicare_number(self):
        return self._medicare_number

    def get_appointment_list(self):
        return self._appointment_list

    def get_full_name(self):
        return self._full_name

    def set_medicare_number(self, new_medicare_number):
        self._medicare_number = new_medicare_number

    def add_appointment(self, appointment):
        self._appointment_list.append(appointment)
        self._num_appointments += 1

    def remove_appointment(self, appointment):
        self._appointment_list.remove(appointment)
        self._num_appointments -= 1

    def __str__(self):
        return str("name: " + self._full_name)


class HealthCareProvider(User):
    """docstring for ClassName"""

    def __init__(self, full_name="", email_address="", phone_number="", provider_number="", type="", working_centre=[],
                 rating="", is_provider=1):
        super().__init__(full_name, email_address, phone_number, is_provider)
        # removed password
        self._is_provider = 1
        self._provider_number = provider_number
        self._type = type
        self._working_centre = working_centre
        self._rating = rating

    # getters
    def get_provider_number(self):
        return self._provider_number

    def get_type(self):
        return self._type

    def get_working_centre(self):
        return self._working_centre

    def get_full_name(self):
        return self._full_name

    def get_appointment_list(self):
        return self._appointment_list

    def get_email_address(self):
        return self._email_address
        # setters

    def set_provider_number(self, new_provider_number):
        self._provider_number = new_provider_number

    def set_type(self, new_type):
        self._type = new_type

    def set_working_centre(self, new_working_centre):
        self._working_centre = new_working_centre

    def add_centre(self, centre):
        current = self._working_centre.copy()
        current.append(centre)
        self._working_centre = current
        self._working_centre = list(set(self._working_centre))

    def add_appointment(self, appointment):
        self._appointment_list.append(appointment)

    def remove_appointment(self, appointment):
        self._appointment_list.remove(appointment)
        self._num_appointments -= 1

    def match_provider(self, search):
        if search == self.get_full_name() or search == self.get_email_address() or search == self.get_type():
            return 1
        return 0

    def __str__(self):
        # return str("name: " + self._full_name + " | type: " + self._type)
        return str(self._full_name + ", " + self._type)
