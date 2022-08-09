# how to use css in python_ flask
# flask render_template example
from apiWeather import *
from flask import Flask, render_template, flash, redirect, request, url_for, session
from forms import SettingsForm
import json
import SendLocations
import os.path

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = '5d8d01ee0f29e7ad312f7ce37568e551'


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    loc_data = request.form.get('modal-input')
    if request.method == 'POST':
        #Search the restuaraunt choices from loc_data and store session
        locationInfo = getLocationInformation(loc_data)
        session["location-data"] = locationInfo
        #Search the milkshake weather from loc_data and store session
        milkshakeInfo = getMilkshakeWeather(loc_data)
        session["weather-data"] = milkshakeInfo
        return render_template('home.html', title='Home', locData=locationInfo, weatherData=milkshakeInfo)
    #Load the cached results from json, if it exists
    locData = None
    weatherData = ''
    #If cached data exists, render template with this data
    if os.path.isfile('./milkshakeInfo.txt') and os.path.isfile('./locationData.json'):
        with open('locationData.json', 'r') as f:
            locData = json.loads(f.read())
        with open('milkshakeInfo.txt', 'r') as f:
            weatherData = f.read()
        return render_template('home.html', title='Home', locData=locData, weatherData=weatherData)
    #Otherwise check if sessions have been saved, and populate with that
    elif 'location-data' in session and 'weather-data' in session:
        location = session["location"]
        weather = session["weather"]
        return render_template('home.html', title='Home', locData=location, weatherData=weather)
    #No cahced data, so render defaults
    else:
        print('No cached data to load')
        return render_template('home.html', title='Home', locData=None, weatherData=None)


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == 'GET':
        return render_template('settings.html', title='Settings')
    if request.method == 'POST':
        loc_data = request.form.get('location-input')
        #Search the restuaraunt choices from loc_data and store session
        locationInfo = getLocationInformation(loc_data)
        session["location-data"] = locationInfo
        #Search the milkshake weather from loc_data and store session
        milkshakeInfo = getMilkshakeWeather(loc_data)
        session["weather-data"] = milkshakeInfo

    return render_template('settings.html', title='Settings')


@app.route('/locations', methods=['POST', 'GET'])
def locations():
    return render_template('locations.html', title='Locations')


@app.route('/information', methods=['POST', 'GET'])
def information():
    return render_template('information.html', title='Information')


@app.route('/settings_input', methods=['POST', 'GET'])
def settings_input():
    if request.method == 'GET':
        form = SettingsForm()
        #return f"The location /data is accessed directly. Try going to '/settings_input' to submit location"
        return render_template('settings_input.html', title='settings_input', form=form)
    if request.method == 'POST':
        #Check settings form input and use 'location' entry to call microservice
        form = SettingsForm()
        form_data = request.form.get('location')
        print(form_data)
        milkshake_rpc = SendLocations.MilkshakeRpcClient()
        response = milkshake_rpc.call(form_data)
        #MUST STRIP THE BODY CHARS ADDED BY RABBIT MQ, AND NULL TERMINATOR
        response = response[2:-1]
        response = json.loads(response)
        print(" [.] Got %r" % response)
        for loc in response:
            print(response[loc])
        return redirect(url_for('home', response=response))


def getMilkshakeWeather(loc_data):
    milkshake_rpc = WeatherRpcClient()
    milkshakeInfo = milkshake_rpc.call(loc_data)
    milkshakeInfo = milkshakeInfo[2:-1]
    inCity = ' in ' + loc_data + '\n'
    milkshakeInfo += inCity
    with open('milkshakeInfo.txt', 'w') as outfile:
        outfile.write(milkshakeInfo)
    return milkshakeInfo


def getLocationInformation(loc_data):
        milkshake_rpc = SendLocations.MilkshakeRpcClient()
        response = milkshake_rpc.call(loc_data)
        response = response[2:-1]
        response = json.loads(response)

if __name__=='__main__':
    #If executed from python directly, do so in debug mode
    app.run(debug = True)
