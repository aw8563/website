class  UnauthAccess(Exception):
    pass
    # can have def __init__(): and __str__() for error messages

class BookingError(Exception):
    pass
def checkBooking(WorksAt, start, end, centre, providerEmail, patientEmail):
    try:
        error = WorksAt.are_valid_hours(start, end, centre, providerEmail, patientEmail)
        if error != '':
            raise BookingError(error)

    except BookingError as error_message:
        print(BookingError)
    else :
        return True


def checkViewHistory(provider, patient):
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

