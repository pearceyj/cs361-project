# how to use css in python_ flask
# flask render_template example
from apiWeather import *
from flask import Flask, render_template, flash, redirect, request, url_for, session
from forms import SettingsForm
import json
import SendLocations
app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = '5d8d01ee0f29e7ad312f7ce37568e551'


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    #Load the cached results from json, if it exists
    locData = None
    weatherData = ''

    if 'location-data' in session and 'weather-data' in session:
        location = session["location"]
        weather = session["weather"]
        return render_template('home.html', title='Home', locData=location, weatherData=weather)
    else:
        return render_template('home.html', title='Home', locData=None, weatherData=None)
    # try:
    #     with open('locationData.json', 'r') as f:
    #         locData = json.loads(f.read())
    #     with open('milkshakeInfo.txt', 'r') as f:
    #         weatherData = f.read()
    # except:
    #     print("No text data to load")
    #
    # if locData:
    #     return render_template('home.html', title='Home', locData=locData, weatherData=None)
    # if locData is not None and weatherData is not None:
    #     return render_template('home.html', title='Home', locData=locData, weatherData=weatherData)
    # else:
    #     return render_template('home.html', title='Home', locData=None, weatherData=None)




@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == 'POST':
        loc_data = request.form.get('location-input')
        milkshake_rpc = SendLocations.MilkshakeRpcClient()
        response = milkshake_rpc.call(loc_data)
        response = response[2:-1]
        response = json.loads(response)
        session["location-data"] = response

        milkshake_rpc = WeatherRpcClient()
        milkshakeInfo = milkshake_rpc.call(loc_data)
        milkshakeInfo = milkshakeInfo[2:-1]
        milkshakeInfo += '\n'
        with open('milkshakeInfo.txt', 'w') as outfile:
            outfile.write(milkshakeInfo)
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


def cacheLocation(milkshakeInfo):
    #Output to JSON for cached access
    with open('milkshakeInfo.json', 'w') as outfile:
        json.dump(milkshakeInfo, outfile, indent = 4)
        print("Creating JSON file from weather data...")

if __name__=='__main__':
    #If executed from python directly, do so in debug mode
    app.run(debug = True)
