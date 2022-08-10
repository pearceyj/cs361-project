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

#webdriver path for local driver use (default in function is to download)
PATH = "C:\\Users\\GilliganMuscaria\\Documents\\school\\summer22\\CS_361\\Team_23\\Assignment_3\\cs361-project\\public\\chromedriver.exe"

def searchCityState(city_state, driver=None):
    #if not passed in, default driver is installed from chrome server (slower)
    if driver == None:
        driver = getUpdatedDriver()

    #Initiate search terms
    searchId = 'q' #google search box identifier
    driver.get("https://www.google.com")
    search_box = driver.find_element('name', searchId)
    search_box.send_keys('Restaurants with milkshakes in' + city_state)
    search_box.submit()

    namesId = 'OSrXXb' #div class on page that hold restaurant names
    locationNames = getLocationNames(driver, namesId)

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


def getUpdatedDriver(options=None):
    #default options are windowless/headless browser
    if options == None:
        options = Options();
        options.add_argument("--headless")
    print("Installing current web driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("Web driver installed!")
    return driver


def initWebDriver(path=None):
    options = Options();
    options.add_argument("--headless")
    if path == None:
        driver = getUpdatedDriver(options)
    else:
        driver = webdriver.Chrome(path, options=options)
    return driver


def getLocationNames(driver, div):
    try:
        #Wait 10 secs for main div to appear before searching
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main'))
        )
        body = main.find_element(By.CLASS_NAME, 'e9EfHf') #Main body div
        locations = body.find_elements(By.CLASS_NAME, 'rllt__details')#contains locations
        locationNames = []
        for location in locations:
            restaurant_name = location.find_element(By.CLASS_NAME, div)
            if restaurant_name is not None:
                locationNames.append(restaurant_name.text)
                print(restaurant_name.text)
            else:
                print("There was a problem finding location names")
    except:
        print("Something went wrong with location search...")
        return None
    finally:
        driver.quit()

    return locationNames

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


    driver = initWebDriver(PATH)
    #Scrape locations, format results, and send message through channel
    locationNames = (searchCityState(bod_str, driver=driver))
    locationFormatted = locationJson(locationNames)

    if locationFormatted != None:
        response = locationFormatted
        print("Generating reponse!")
    else:
        response = "Request Failed"
        return None
    #Important to dump json here for JSON to send properly, must load on other end
    ch.basic_publish(exchange='', routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('Message sent!')

#Begin consuming incoming messages indefinitely
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='myMilkShakes', on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
