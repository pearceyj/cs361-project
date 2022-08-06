# how to use css in python_ flask
# flask render_template example

from flask import Flask, render_template, flash, redirect, request
from forms import SettingsForm
import json
import SendLocations
app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = '5d8d01ee0f29e7ad312f7ce37568e551'





@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/settings')
def settings():
    return render_template('settings.html', title='Settings')


@app.route('/settings_input', methods=['POST', 'GET'])
def settings_input():
    if request.method == 'GET':
        form = SettingsForm()
        #return f"The location /data is accessed directly. Try going to '/settings_input' to submit location"
        return render_template('settings_input.html', title='settings_input', form=form)
    if request.method == 'POST':
        form = SettingsForm()
        form_data = request.form.get('location')
        print(form_data)
        milkshake_rpc = SendLocations.MilkshakeRpcClient()
        response = milkshake_rpc.call(form_data)
        # #MUST STRIP THE BODY CHARS ADDED BY RABBIT MQ, AND NULL TERMINATOR
        response = response[2:-1]
        print(" [.] Got %r" % json.loads(response))
        return render_template('settings_input.html', title='settings_input', form=form)




if __name__=='__main__':
    app.run(debug = True)
