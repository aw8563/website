class  UnauthAccess(Exception):
    pass
    # can have def __init__(): and __str__() for error messages
def  checkViewHistory(provider, patient):

    try:
        if (provider.role == 'Patient'):
            raise UnauthAccess("you need to be a provider to view this")

        permission = False
         
        for b in patient.provider_bookings:
            
            if (b.provider_email == provider.email):
                permission = True
        if not permission:
            raise UnauthAccess("you need a booking with patient to have access")

    except UnauthAccess as error_message:

        print (error_message)
        return False
    else:
        print("no problems")
        return True
    

#check line 479 in routes

