from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response  #todo: use cookies!
import io
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import requests

app = Flask(__name__)
"""
set environment variable $ROULETTE_SETTINGS to point to a file
containing your desired configuration
"""
app.config.from_envvar('ROULETTE_SETTINGS', silent=True)

@app.route('/')
def index(name=None):
    # payload = {'location':'wicker park',
    #            'description':'coffee',
    #            'time' : 3
    #           }
    # r = requests.get('https://127.0.0.1:5000/query',params=payload)
    return render_template('layout.html',name=name)

@app.route('/query', methods='GET')
def query():
    error = None
    if request.method =='GET':
        if valid_request(request.form['location'],
                        request.form['description'],
                        request.form['time']):
            return fulfill_query_request(request.form['location'],
                            request.form['description'],
                            request.form['time'])
        else:
            #handle error on bad request
            #(maybe just do this on the client side)
            return render_template('index.html', error=error)

def valid_request(location,description,time):
    """check if location,description, and time are set for a request"""
    return all([location,description,time])

def fulfill_query_request(location, description, time):
    """use yelp api to fulfill a request"""
    client = authenticate_api()
    print location
    print description
    print time
    if client is None:
        #handle error
        print "uh oh!"
        return None
    params = {
        'terms' : query,
        'lang'  : 'en' #todo: let user pick!
    }
    #todo: properly choose whether to search by bounded box or not!
    #ex: let user pick multiple locations and make a box that encompasses
    #them
    response = client.search(location, **params)
    #do some work . . . . .
    if response is None:
        return None #todo handle error
    response_dict = {}
    response_keys = ['businesses','addresses',
                           'phone numbers','ratings',
                           'review counts']

    response_values = []
    for key in response_keys:
        response_values.append(list(business.__dict__[key] for business in blist))
    print response_values


def authenticate_api():
    """check credentials and return a yelp client"""
    with io.open('static/yelp_config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
    return client

if __name__ == '__main__':
    app.debug = True
    app.run()
