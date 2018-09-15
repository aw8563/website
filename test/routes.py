from server import app, valid_time
from flask import request, render_template


@app.route('/', methods = ['GET', 'POST'])
def home():
    
    list1 = ["a", "b", "c"]

    if (request.method == 'POST'): #redirect to the search screen
        print("hi")
        return render_template('results.html', display = list1)
    



    return render_template('search.html', title = 'home')
