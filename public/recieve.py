#!/usr/bin/env python
import pika, sys, os, requests, json
api_key="fd104cbd085aea7da712982efb90f497"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='myQueue')
channel.queue_purge('myQueue')
def callback(ch, method, props, body):
    bod_str = str(body)

    commaPos = bod_str.find(",")
    if commaPos == -1:
        bod_str = bod_str[1:]
        print(bod_str)
        loc_url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + bod_str + '&appid=' + api_key
    else:
        city = bod_str[0:commaPos]
        state = bod_str[(commaPos+1):]

        loc_url = 'http://api.openweathermap.org/data/2.5/forecast?lat=' + city + '&lon=' + state + '&appid=' + api_key + '&units=imperial'

    loc_info = requests.get(loc_url)
    location = json.loads(loc_info.text)

    if len(location)>0:
        lat = str(location[0]['lat'])
        lon = str(location[0]['lon'])

        weath_url = 'http://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + lon + '&appid=' + api_key + '&units=imperial'
        weath_info = requests.get(weath_url)
        weather = json.loads(weath_info.text)

        if weather['cod'] == '200':
            feels_like = weather['list'][0]['main']['feels_like']
            description = weather['list'][0]['weather'][0]['description']
            print(feels_like)
            print(description)
            if int(feels_like)>=85 and (description=='clear sky' or description=="few clouds"):
                response = "It is Milkshake Weather"
            else:
                response = "Not Milkshake Weather"
        else:
            response = "Could not find weather"
    else:
        response = "Request Failed"

    ch.basic_publish(exchange='', routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),body=response)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='myQueue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


