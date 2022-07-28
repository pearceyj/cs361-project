#!/usr/bin/env python
import pika, sys, os, requests, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Should install chromedriver automatically from server (slower), or can be
# modified to use existing chromedriver (faster, but creates dependency)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import time

import json #for exporting locationData to json

def searchCityState(city_state):
    formatList = ['Name']
    locationData = {}
    for i in formatList:
        locationData[i] = None

    #make browser headless, so no window pops up
    options = Options();
    options.add_argument("--headless")
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    #driver = webdriver.Chrome(PATH)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #open google for search
    driver.get("https://www.google.com")
    #prints the title of the driver
    #print(driver.title)

    #specified location [city, state] to search
    #city_state is location sent as following format: 'Albany, Oregon'
    #However, it is very forgiving and will accept any name
    #google search bar, with html attribute name 'q'
    search_box = driver.find_element('name', 'q')
    #Search string with the requested city, state
    search_box.send_keys('Restaurants with milkshakes in'  + city_state)
    #enter the search, like pressing enter
    search_box.submit()

    #print(driver.page_source)

    try:
        #Wait for main div to appear before searching
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main'))
        )
        # go to largest div in main div
        body = main.find_element(By.CLASS_NAME, 'e9EfHf')
        #g
        #go to div containing top 3 results
        locations = body.find_elements(By.CLASS_NAME, 'rllt__details')
        #Grab the names of the restaurant results, store them in list and print
        locationNames = []
        locationString = ''
        for location in locations:
            restaurant_name = location.find_element(By.CLASS_NAME, 'OSrXXb')
            locationNames.append(restaurant_name.text)

        restaurants = str()
        listLength = len(locationNames)
        for name in range (listLength):
            print(locationNames[name])
            restaurants += locationNames[name] + ','
        restaurants = restaurants[:-1]


    except:
        print("Something went wrong")
    finally:
        driver.quit()

    #print(locationNames)
    #return locationNames
    return restaurants


#RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='myQueue')
channel.queue_purge('myQueue')
def callback(ch, method, props, body):
    """
    Messaging queue. Recieves location and responds with milkshake Restaurants
    in the area
    """
    bod_str = str(body)

    commaPos = bod_str.find(",")
    if commaPos == -1:
        bod_str = bod_str[1:]
        print(bod_str)
        city_state = bod_str
    else:
        city = bod_str[0:commaPos]
        state = bod_str[(commaPos+1):]
        city_state = city + ', ' + state

    locationNames = searchCityState(city_state)

    if city_state != None:
        response = locationNames
    else:
        response = "Request Failed"

    ch.basic_publish(exchange='', routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),body=str(response))

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='myQueue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
