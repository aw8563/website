class HealthCareCentre:
    """docstring for health_care_centre"""

    def __init__(self, name="", suburb="", phone="", service="", rating="", type="", provider_list=[], abn=""):
        self._name = name
        self._suburb = suburb
        self._phone = phone
        self._service = service
        self._rating = rating
        self._type = type
        self._provider_list = provider_list
        self._is_user = 0
        self._abn = abn

    # getters
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

    def get_provider_list(self):
        return self._provider_list

    # setters
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

    def set_provider_list(self, new_provider_list):
        self._provider_list = new_provider_list

    def add_provider(self, new_provider):
        cpy = self.get_provider_list().copy()
        cpy.append(new_provider)
        self.set_provider_list(cpy)

    def match_centre(self, search):
        if (search == self.get_name() or search == self.get_suburb() or search == self.get_type()):
            return 1
        return 0

    def __str__(self):
        # string = "Name: " + self._name + " | Type: " + self._type + " | Suburb: " + self._suburb
        string = self._name
        return str(string)
