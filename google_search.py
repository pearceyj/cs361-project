from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import time




PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#open google for search
driver.get("http://www.google.com")
#print(driver.title)

#specified location [city, state] to search
city_state_name = 'Hawaii'
#google search bar, with html attribute name 'q'
search_box = driver.find_element('name', 'q')
#Search string with the requested city, state
search_box.send_keys('Restaurants with milkshakes in'  + city_state_name)
search_box.submit()

#print(driver.page_source)
#Wait for main div to appear before searching
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'main'))
    )
    # go to largest div in main div
    next_frame = main.find_element(By.CLASS_NAME, 'e9EfHf')
    #go to div containing top 3 results
    locations = next_frame.find_elements(By.CLASS_NAME, 'rllt__details')
    #Grab the names of the restaurant results
    for location in locations:
        restaurant_name = location.find_element(By.CLASS_NAME, 'OSrXXb')
        print(restaurant_name.text)
finally:
    driver.quit()
# listing = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='OSrXXb']")))
# listing = driver.find_element(By.CLASS_NAME, 'OSrXXb')
# for elem in listing:
#     print("Location name" + listing.text)

#"//span[@class='OSrXXb']" ##location in html of top 3 results
#driver.close() #closes the webpage
