# MyMilkshakes (CS 361)
How to use Micro Service Note: 

REQUEST

Add MilkshakeRpcClient() class in the main body of your application
Instantiate MilkshakeRpcClient object in backend
Use function to cal .call() method of class object or call it directly passing in location string
String must be city i.e. "Sandiego" or city and state seperated with comma and without spacing i.e. "Sandiego,CA"

RECIEVE

.call() method will pass the location message along to my backend process to source local restaurants that serve milkshakes.

The backened microservice will deploy a web-scraper to capture the top 3 milkshake locations based upon the location from the message.

The format is very forgiving and can gather reliable results without strictly enforced syntax, but it would be best to stick to the following formats:

-"City, State"
  -e.g., "Albany, oregon" (Most reliable, space after comma is optional)
-"City"
  -e.g, "Crescent City" (best use for well-known cities or unique city names)
-"State"
  -e.g., "California" (Will return much broader results, though that may be desired)

The response will be in the following format:

JSON file containing a dictionary with the following keys (values for example, taken from Redding, CA search):

{
    "loc1": "Dudes Drive Inn", 
    "loc2": "Dairy Queen Grill & Chill", 
    "loc3": "Damburger"
}
  
Note: this service does not cache previous results, and may take up to 10 seconds to recieve a response due to the use of a webdriver that powers the web-scraping process.
  
