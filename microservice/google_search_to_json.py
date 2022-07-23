from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import time

import json #for exporting locationData to json



def getNames():
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
        #print out the list of names
        # listLength = len(locationNames)
        # for x in range (listLength):
        #     print(locationNames[x])
    except:
        print("Something went wrong")
    finally:
        driver.quit()

    return locationNames

#initialize list for storing location data
#formatList = ['Name', 'Rating', 'Address', 'Hours', "TopReview"]
#limiting to just names for now, above list is whole thing
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
print(driver.title)

#specified location [city, state] to search
city_state_name = 'Albany, Oregon'
#google search bar, with html attribute name 'q'
search_box = driver.find_element('name', 'q')
#Search string with the requested city, state
search_box.send_keys('Restaurants with milkshakes in'  + city_state_name)
#enter the search, like pressing enter
search_box.submit()

#print(driver.page_source)

locationNames = getNames()
print(locationNames)

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

#Dump the data in JSON format for writing to file
# final = json.dumps(allLocations, indent=4)
#Open the file and write the data
with open('locationData.json', 'w') as outfile:
    json.dump(allLocations, outfile, indent = 4)

with open('locationData.json', 'r') as infile:
    locations = json.loads(infile.read())
for name in locations:
    print(name)
