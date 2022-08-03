# how to use css in python_ flask
# flask render_template example

from flask import Flask, render_template
import json
import SendLocations

# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templates', static_folder='static')

# @app.route('/')
# def welcome():
#     return "This is the home page of Flask Application"

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')

# milkshake_rpc = SendLocations.MilkshakeRpcClient()
# #
# response = milkshake_rpc.call("Albany, Oregon")
# # #MUST STRIP THE BODY CHARS ADDED BY RABBIT MQ, AND NULL TERMINATOR
# response = response[2:-1]
# print(" [.] Got %r" % json.loads(response))

if __name__=='__main__':
    app.run(debug = True)
