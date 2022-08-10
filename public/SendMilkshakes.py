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


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form.get('modal-location'):
            loc_data = request.form.get('modal-location')
            locationInfo = getLocationInformation(loc_data)
            session["location-data"] = locationInfo
            milkshakeInfo = getMilkshakeWeather(loc_data)
            session["weather-data"] = milkshakeInfo
            return redirect(url_for('home'))
    return render_template('home.html', title='index', locData=None, weatherData=None, showCow=None, showWeather="off", showLocationModal = True)


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.method == 'POST':
            cowBox = request.form.get('cow-box')
            print(cowBox)
            session["cow-box"] = cowBox
            weatherBox = request.form.get('weather-box')
            print(weatherBox)
            session["weather-box"] = weatherBox
            #Search the restuaraunt choices from loc_data and store session
            if request.form.get('location-input'):
                loc_data = request.form.get('location-input')
                print(loc_data)
                locationInfo = getLocationInformation(loc_data)
                session["location-data"] = locationInfo
                #Search the milkshake weather from loc_data and store session
                milkshakeInfo = getMilkshakeWeather(loc_data)
                session["weather-data"] = milkshakeInfo
    #Load session data, otherwise load cached data and render home page
    locData = retrieveLocationData()
    weatherData = retrieveWeatherData(session)
    showCow = retrieveShowCow(session)
    showWeather = retrieveShowWeather(session)
    return render_template('home.html', title='Home', locData=locData, weatherData=weatherData, showCow=showCow, showWeather=showWeather)


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == 'GET':
        return render_template('settings.html', title='Settings')
    if request.method == 'POST':
        cowBox = request.form.get('cow-box')
        print(cowBox)
        session["cow-box"] = cowBox
        weatherBox = request.form.get('weather-box')
        print(weatherBox)
        session["weather-box"] = weatherBox
        #Search the restuaraunt choices from loc_data and store session
        if request.form.get('location-input'):
            loc_data = request.form.get('location-input')
            print(loc_data)
            locationInfo = getLocationInformation(loc_data)
            session["location-data"] = locationInfo
            #Search the milkshake weather from loc_data and store session
            milkshakeInfo = getMilkshakeWeather(loc_data)
            session["weather-data"] = milkshakeInfo
    return redirect(url_for('home'))
    # return render_template('settings.html', title='Settings')


@app.route('/locations', methods=['POST', 'GET'])
def locations():
    return render_template('locations.html', title='Locations')


@app.route('/information', methods=['POST', 'GET'])
def information():
    return render_template('information.html', title='Information')


def getMilkshakeWeather(loc_data):
    milkshakeInfo = None
    milkshake_rpc = WeatherRpcClient()
    milkshakeInfo = milkshake_rpc.call(loc_data)
    if milkshakeInfo != None:
        milkshakeInfo = milkshakeInfo[2:-1]
        inCity = ' in ' + loc_data + '\n'
        milkshakeInfo += inCity
        #cache data for later use
        with open('milkshakeInfo.txt', 'w') as outfile:
            outfile.write(milkshakeInfo)
    return milkshakeInfo


def getLocationInformation(loc_data):
    response = None
    if loc_data != None:
        milkshake_rpc = SendLocations.MilkshakeRpcClient()
        response = milkshake_rpc.call(loc_data)
        response = response[2:-1]
        print(response)
        response = json.loads(response)
    return response


def retrieveWeatherData(session):
    weatherData = None
    if "weather-data" in session:
        print("Reading weatherData from Session")
        weatherData = session["weather-data"]
    elif os.path.isfile('./milkshakeInfo.txt'):
        with open('milkshakeInfo.txt', 'r') as f:
            print("Reading weatherData from JSON")
            weatherData = f.read()
    return weatherData


def retrieveLocationData():
    locData = None
    if os.path.isfile('./locationData.json'):
        with open('locationData.json', 'r') as f:
            print("Reading locationData from JSON")
            locData = json.loads(f.read())
    return locData


def retrieveShowCow(session):
    showCow = None
    if "cow-box" in session:
        print("Reading showCow from Session")
        showCow = session["cow-box"]
    return showCow


def retrieveShowWeather(session):
    showWeather = None
    if "weather-box" in session:
        print("Reading showWeather from Session")
        showWeather = session["weather-box"]
    return showWeather


if __name__=='__main__':
    #If executed from python directly, do so in debug mode
    app.run(debug = True)
