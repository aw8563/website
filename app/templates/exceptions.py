def UnauthAccess(Exception):
    def __init__(self, error_message):
        self.error = error_message
    
    def __str__(self)
        return str("ERROR: " + self.error_message)


def checkViewHistory(provider, patient):
    try:
        permission = False
        for b in patient.patient_bookings: # and also booked with the patient  
            if (b.patient_email == provider.email):
                permission = True
        if not permission:
            raise UnauthAccess("You do not have access to this page") 

        except UnauthAccess as error_message:
            print(error_message):
            return render_template('error.html', error = error_message)
        finally
            print("no problems")
