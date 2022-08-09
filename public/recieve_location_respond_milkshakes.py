#!/usr/bin/env python
import pika, sys, os, requests, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

#Alternate chrome webdriver PATH setup:
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def searchCityState(city_state, driver=None):
    """
    Recieves: city_state in format "City, State"
    Returns:  locationData of top 3 milkshake location in area, as dictionary
    """
    #Alternate chrome webdriver PATH setup:
    PATH = "C:\\Users\\GilliganMuscaria\\Documents\\school\\summer22\\CS_361\\Team_23\\Assignment_3\\cs361-project\\public\\chromedriver.exe"
    options = Options(); #make browser headless/windowless
    options.add_argument("--headless")
    driver = webdriver.Chrome(PATH, options=options)
    #Initiate search terms
    driver.get("https://www.google.com")
    search_box = driver.find_element('name', 'q')
    search_box.send_keys('Restaurants with milkshakes in'  + city_state)
    search_box.submit()

    try:
        #Wait 10 secs for main div to appear before searching
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main'))
        )
        body = main.find_element(By.CLASS_NAME, 'e9EfHf') #Main body div
        locations = body.find_elements(By.CLASS_NAME, 'rllt__details')#contains locations
        locationNames = []
        for location in locations:
            restaurant_name = location.find_element(By.CLASS_NAME, 'OSrXXb')
            if restaurant_name is not None:
                locationNames.append(restaurant_name.text)
            else:
                print("There was a problem finding location names")
    except:
        print("Something went wrong")
        return None
    finally:
        driver.quit()

    return locationNames


def locationJson(locationNames):
    #Directly write in values becuase they always come in 3's
    locationDict = {
        "loc1" : None,
        "loc2" : None,
        "loc3" : None
    }
    #Strip apostrophes because RabbitMQ sends json as string causes errors
    if locationNames is not None:
        locationDict["loc1"] = locationNames[0].replace("'","").replace('"', '')
        locationDict["loc2"] = locationNames[1].replace("'","").replace('"', '')
        locationDict["loc3"] = locationNames[2].replace("'","").replace('"', '')
    #Output to JSON for cached access
    with open('locationData.json', 'w') as outfile:
        json.dump(locationDict, outfile, indent = 4)
        print("Creating JSON file from location data...")

    return locationDict


#RabbitMQ, initialize communication pipeline
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='myMilkShakes')
channel.queue_purge('myMilkShakes')

def callback(ch, method, props, body):
    """
    Messaging queue. Recieves location and responds with milkshake Restaurants
    in the area
    """
    bod_str = str(body)

    #perform the web scraping search, format results, and send message through channel
    locationNames = (searchCityState(city_state))
    locationFormatted = locationJson(locationNames)

    if locationFormatted != None:
        response = locationFormatted
        print("Generating reponse!")
    else:
        response = "Request Failed"
        return "Something went wrong with response. Delivery failed."
    #Important to dump json here for JSON to send properly, must load on other end
    ch.basic_publish(exchange='', routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),body=json.dumps(response))

    ch.basic_ack(delivery_tag=method.delivery_tag)

#Begin consuming incoming messages indefinitely
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='myMilkShakes', on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
