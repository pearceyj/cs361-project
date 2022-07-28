# MyMilkshakes (CS 361)
How to use Micro Service Note: 

REQUEST

You must create a  MilkshakeRpcClient() class in the main body of your application

Be sure to declare a MilkshakeRpcClient object in backend

Pass in the location as the sole argument to the .call() function on your MilkshakeRpcClient class object.

String does not need to adhere to stric syntax, but the more specific the better the results you will recieve.

EXAMPLE:

#Testing request milkshake location service; sends location by city, state
milkshake_rpc = MilkshakeRpcClient()

response = milkshake_rpc.call("Redding, California")

#You must strip the first 2 chars from the respons string, due to how RabbitMQ places body-designating chars at the beginning. It is also important to remove the null terminator at the end of the string, before the response may be loaded as a JSON.USe the method below:

response = response[2:-1]
print(" [.] Got %r" % json.loads(response))

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
  
![MyMilkshakesUML](https://user-images.githubusercontent.com/86382179/181436708-d2e8d528-3bd7-47e1-a021-03702198aefa.png)
