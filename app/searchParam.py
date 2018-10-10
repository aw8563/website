class SearchParam:
    def __init__(self, centre_name, provider_name, suburb, centre_type, provider_type, \
                 view_provider, view_centre):
        self._provider_name = provider_name
        self._centre_name = centre_name
        self._suburb = suburb
        self._centre_type = centre_type
        self._provider_type = provider_type
        self._view_provider = view_provider
        self._view_centre = view_centre

    def centre_type(self):
        return self._centre_type
    def provider_type(self):
        return self._provider_type
    def suburb(self):
        return self._suburb
    def provider_name(self):
        return self._provider_name
    def centre_name(self):
        return self._centre_name
    

    # returns matchinig results from a given list of centres and providers    
    def results(self, centres, providers):
        centreResults = []
        providerResults = []
        pName = normalise(self._provider_name)
        cName = normalise(self._centre_name)
        suburb = normalise(self._suburb)
        cType = normalise(self._centre_type)
        pType = normalise(self._provider_type)

        centresCopy = centres.copy()
        providersCopy = providers.copy()

                


        c = 0
        p = 0

        if (cType != "" or cName != "" or suburb != ""): # ignore if all fields are empty
            c = 1

        if (c):
            print("made it here")
            for c in centresCopy:

                # dealing with empty inputs
                if self._centre_name == "":
                    cName = normalise(str(c._name))
                if self._centre_type == "":
                    cType = normalise(str(c._type))
                if self._suburb == "":
                    suburb = normalise(str(c._suburb))          
                # matching the search criteria
                if cName in normalise(c._name) and cType in normalise(c._type) \
                   and suburb in normalise(c._suburb) and cName[0] == c._name[0].lower() \
                   and cType[0] == c._type[0].lower() and suburb[0] == c._suburb[0].lower():
                    centreResults.append(c)
        

        if (pName != "" or pType != ""):
            p = 1
        if (p):
            for p in providersCopy:
                # dealing with empty inputs
                if self._provider_name == "":
                    pName = normalise(p._full_name)
                if self._provider_type == "":
                    pType = normalise(p._type)
                
                # matching the search criteria
                if pName in normalise(p._full_name) and pType in normalise(p._type) and \
                   pName[0] == p._full_name[0].lower() and pType[0] == p._type[0].lower():
                    providerResults.append(p)

        # add all providers from matching hospitals
        if self._view_provider and p == 0:
            for c in centreResults:
                for p in c._providerList:
                    providerResults.append(p)

        # add all working centres from matching providers   
        if self._view_centre and c == 0:
            for p in providerResults:
                for c in p._working_centre:
                    centreResults.append(c)        

        return [centreResults,providerResults]

    def __str__(self):  
        string = "|%s |%s |%s |%s |%s |%s |%s aa" % (self._centre_name, self._provider_name, \
                                           self._suburb, self._centre_type, \
                                           self._provider_type, self._view_provider, \
                                           self._view_centre)
        return string

# takes the returned string from the SearchParam and converts it back into an object class
def makeSearchObject(string):
    split = string.split()
    result = []
    for words in split:
        result.append(words[1:])
    
    return SearchParam(result[0], result[1], result[2], result[3], \
                       result[4], int(result[5]), int(result[6]))
# removes spaces and converts to lower case for comparison
def normalise(string):
    string = string.lower()
    string = string.replace(" ", "")
    string = string.replace("\t", "")
    return string
