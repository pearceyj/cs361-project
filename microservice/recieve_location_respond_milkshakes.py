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
        for location in locations:
            restaurant_name = location.find_element(By.CLASS_NAME, 'OSrXXb')
            locationNames.append(restaurant_name.text)
    except:
        print("Something went wrong")
        return None
    finally:
        driver.quit()

        #grab names and store into list
        numLocations = len(locationNames)
        #create master lsit to hold all location dictionary info

        allLocations = [{} for sub in range(numLocations)]
        for i in range (numLocations):
            print(locationNames[i])
            allLocations[i]['Name'] = locationNames[i]

        #Print out the stored values to confirm valid
        for i in range(len(allLocations)):
            print(allLocations[i])

        #Directly write in values becuase they always come in 3's
        locationDict = {
            "loc1" : None,
            "loc2" : None,
            "loc3" : None
        }
        #Strip apostrophes because RabbitMQ sends json as string and we get errors
        locationDict["loc1"] = locationNames[0].replace("'","").replace('"', '')
        locationDict["loc2"] = locationNames[1].replace("'","").replace('"', '')
        locationDict["loc3"] = locationNames[2].replace("'","").replace('"', '')
        #Dump the data in JSON format for writing to file
        with open('locationData.json', 'w') as outfile:
            json.dump(allLocations, outfile, indent = 4)
            print("Creating JSON file from location data...")
        #Open the file and write the data
        # with open('locationData.json', 'r') as infile:
        #     locations = json.loads(infile.read())
        #     print("Testing onload...\n%r", locations)

        #locationDataJson = json.dumps(locationDict, indent=4)
        #locationsStr = str(locationDataJson)

    #print(locationNames)
    #return locationNames
    return locationDict


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

    locationNames = (searchCityState(city_state))

    if locationNames != None:
        response = locationNames
        print("Returning 'LocationData.json' to sender!")
    else:
        response = "Request Failed"

    ch.basic_publish(exchange='', routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),body=json.dumps(response))

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='myQueue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
