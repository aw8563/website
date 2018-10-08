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
        pName = self._provider_name
        cName = self._centre_name
        suburb = self._suburb
        cType = self._centre_type
        pType = self._provider_type
        
        c = 0
        p = 0

        if (cType != "" or cName != "" or suburb != ""): # ignore if all fields are empty
            c = 1

        if (c):
            print("made it here")
            for c in centres:
                # dealing with empty inputs
                if self._centre_name == "":
                    cName = str(c._name)
                if self._centre_type == "":
                    cType = str(c._type)
                if self._suburb == "":
                    suburb = str(c._suburb)            
                # matching the search criteria
                if cName == c._name and cType == c._type and suburb == c._suburb:
                    centreResults.append(c)

        

        if (pName != "" or pType != ""):
            p = 1
        if (p):
            for p in providers:
                # dealing with empty inputs
                if self._provider_name == "":
                    pName = p._full_name
                if self._provider_type == "":
                    pType = p._type
                
                # matching the search criteria
                if pName == p._full_name and pType == p._type:
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
        return "TRUE"

