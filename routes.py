from server import app, valid_time
from flask import request, render_template
import csv
from classes import *
def matchC(centre, search):
    if (search == centre._name or search == centre._suburb or search == centre._type):
        return 1
    return 0

def matchP(provider, search):
    if (search == provider._full_name or search == provider._email_address or search == provider._type):
        return 1
    return 0

@app.route('/', methods = ['GET', 'POST'])
def home():

    centreList = []
    providerList = []

    with open('centre.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            centreType = row['centre_type']
            centreName = row['name'] 
            centrePhone = row['phone']
            centreID = row['abn'] 
            centreSub = row['suburb']
            centre = health_care_centre(centreName, centreSub, centrePhone,
                     "","", type = centreType)
            centreList.append(centre)
    with open('provider.csv') as g:
        reader = csv.DictReader(g)
        for row in reader:
            email = row['provider_email']
            type = row['provider_type']
            pw = row['password']  
            provider = health_care_provider(email_address = email,type = type, password = pw)
            providerList.append(provider)  



    with open('providerCentre.csv') as g:
        reader = csv.DictReader(g)
        n = 0
        for row in reader:
            n+=1
            email = row['provider_email']
            centre = row['health_centre_name']
            for provider in providerList:    
                if (provider._email_address == email):
                    provider.addCentre(centre)     #add centre to provider

            for c in centreList: # add provider to centre
                if (c._name == centre):
                    c.addProvider(email[0:email.find('@')])
            
    if (request.method == 'POST'): #redirect to the search screen
        search = request.form['search']
        
        results = [] #for centres
        results2 = [] #for providers
        for centres in centreList:
            if (matchC(centres, search)):
                results.append(centres)
                for p in centres._providerList:
                    results2.append(p)
        for providers in providerList:
            if (matchP(providers, search)):
                results2.append(providers)
                for c in providers._working_centre:
                    results.append(c)
                    
        results = list(set(results))
        results2 = list(set(results2))
        if (len(results) > 0 or len(results2) > 0):
            print("RESULTS")
            return render_template('results.html', display = results, display2 = results2)
   
        return render_template('results.html', display = ["EMPTY"],display2 = ["EMPTY"])

    return render_template('search.html', title = 'home')
