import requests
import json
import pika
import uuid

api_key="fd104cbd085aea7da712982efb90f497"
moon_key = "3Y5U94C7DCCYMHKZHFF293Y9W"

class WeatherRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='myQueue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return str(self.response)

def getLoc(*loc_deets):
    if len(loc_deets)==1:
        loc_url = 'http://api.openweathermap.org/geo/1.0/direct?q='+ loc_deets[0] +'&appid='+api_key
    elif len(loc_deets)==2:
        loc_url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + loc_deets[0] + ',' +loc_deets[1]+'&appid=' + api_key
    #elif loc_deets[0] is not False and loc_deets[1] is not False and loc_deets[2] is not False:
        #loc_url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + loc_deets[0] + ',' + loc_deets[1] + ',' + loc_deets[2]+'&appid=' + api_key

    loc_info = requests.get(loc_url)
    location = json.loads(loc_info.text)

    if isinstance((location[0]['name']), str) is True:
        lat = str(location[0]['lat'])
        lon = str(location[0]['lon'])

        weath_url = 'http://api.openweathermap.org/data/2.5/forecast?lat=' + lat +'&lon=' + lon +'&appid='+ api_key +'&units=imperial'

        return (weath_url, lat, lon)

def getWeather(weathReqURL):
    weath_info = requests.get(weathReqURL)
    weather = json.loads(weath_info.text)

    if weather['cod'] == '200':
        return weather
    else:
        x = "get weath failed"
        return x

def getMoon(lat, lon, theDate):
    moonURL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+lat+","+lon+"/"+theDate+"?key="+moon_key
    moonInfo = requests.get(moonURL)
    moon= json.loads(moonInfo.text)
    phase = moon["currentConditions"]["moonphase"]

    if phase == 0:
        phase = "New Moon"
    elif phase>0 and phase<.25:
        phase = "Waxing Crescent"
    elif phase == .25:
        phase = "First Quarter"
    elif phase>.25 and phase<.5:
        phase = "Waxing Gibbous"
    elif phase == .5:
        phase = "Full Moon"
    elif phase > .5 and phase < .75:
        phase = "Waning Gibbous"
    elif phase == .75:
        phase = "Last Quarter"
    elif phase>.75:
        phase = "Waning Crescent"

    return phase

def getAll(*loc_deets):
    latLonInfo = getLoc(*loc_deets)
    milkshake_rpc = WeatherRpcClient()
    milkshakeInfo = milkshake_rpc.call(str(*loc_deets))

    weathInfo = getWeather(latLonInfo[0])

    theDate = weathInfo['city']['sunset']

    moonInfo = getMoon(str(latLonInfo[1]), str(latLonInfo[2]), str(theDate))

    return (weathInfo, moonInfo, milkshakeInfo)

