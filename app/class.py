
class user:
    def __init__(self, full_name = "", email_address = "", phone_number = ""):

        self._full_name = full_name
        self._email_address = email_address
        self._phone_number = phone_number

class patient(user):
    def __init__(self, full_name = "", email_address = "", phone_number = "", medicare_number = ""):
        super().__init__(full_name, email_address, phone_number)
        self._medicare_number = medicare_number

    def get_medicare_number(self):
        return self._medicare_number
    def set_medicare_number(self, new_medicare_number):
        self._medicare_number = new_medicare_number

    def __str__(self):
        return self

class health_care_provider(user):
    """docstring for ClassName"""
    def __init__(self, full_name = "", email_address = "", phone_number = "", provider_number = "", type = "", working_centre = ""):
        super().__init__(full_name, email_address, phone_number)
        self._provider_number = provider_number
        self._type = type
        self._working_centre = working_centre

    #getters
    def get_provider_number(self):
        return self._provider_number
    def get_type(self):
        return self._type
    def get_working_centre(self):
        return self._working_centre
    #setters
    def set_provider_number(self, new_provider_number):
        self._provider_number = new_provider_number 
    def set_type(self, new_type):
        self._type = new_type
    def set_working_centre(self, new_working_centre):
        self._working_centre = new_working_centre   
    def __str__(self):
        return self

class health_care_centre:
    """docstring for health_care_centre"""
    def __init__(self, name = "", suburb = "", phone = "", service = "", rating = "", type = ""):
        self._name = name
        self._suburb = suburb
        self._phone = phone
        self._service = service
        self._rating = rating
        self._type = type

    #getters
    def get_name(self):
        return self._name
    def get_suburb(self):
        return self._suburb
    def get_phone(self):
        return self._phone
    def get_service(self):
        return self._service
    def get_rating(self):
        return self._rating        
    def get_type(self):
        return self._type
        
    #setters
    def set_name(self, new_name):
        self._name = new_name 
    def set_suburb(self, new_suburb):
        self._suburb = new_suburb
    def set_phone(self, new_phone):
        self._phone = new_phone
    def set_service(self, new_service):
        self._service = new_service 
    def set_rating(self, new_rating):
        self._rating = new_rating
    def set_type(self, new_type):
        self._type = new_type 


    def __str__(self):
        return self
class appointment:
    """docstring for appointment"""
    def __init__(self, start_time, end_time, date, patient, health_care_provider, fee):
        self._start_time = start_time
        self._end_time = end_time
        self._date = date
        self._patient = patient
        self._health_care_provider = health_care_provider
        self._fee = fee
    def __str__(self):
        return self


#andy = patient("ANDY WANG", "andy@gmail.com", 000, 111)
#print(andy.get_medicare_number())
#andy.set_medicare_number(1234)
#print(andy.get_medicare_number())
