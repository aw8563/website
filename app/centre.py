class health_care_centre:
    """docstring for health_care_centre"""
    def __init__(self, name = "", suburb = "", phone = "", service = "", ratings = [], type = "", providerList = [], abn = ""):
        self._name = name
        self._suburb = suburb
        self._phone = phone
        self._service = service
        self._ratings = []
        self._type = type
        self._providerList = providerList
        self._isuser = 0
        self._abn = abn

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
        total = 0
        if len(self._ratings) == 0:
            return 0
        for rating in self._ratings:
            total += rating
        return total/len(self._ratings)       
    def get_type(self):
        return self._type
    def get_providerList(self):
        return self._providerList
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
        self._ratings.clear()
        self.add_rating(new_rating)
    def set_type(self, new_type):
        self._type = new_type
    def set_providerList(self, new_providerList):
        self._providerList = new_providerList
    def add_rating(self, rating):
        self._ratings.append(rating)
    def addProvider(self, newProvider):
        cpy = self.get_providerList().copy()
        cpy.append(newProvider)
        self.set_providerList(cpy)
    def matchCentre(self, search):
        if (search == self.get_name() or search == self.get_suburb() or search == self.get_type()):
            return 1
        return 0
    def __str__(self):
        #string = "Name: " + self._name + " | Type: " + self._type + " | Suburb: " + self._suburb
        string = self._name
        return str(string)
        