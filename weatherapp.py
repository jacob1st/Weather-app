# The request library allows us to make GET requests to the weather api
import requests

# get some important weather information from the dictionary or list provided from the response
def format_response(response):
    temp = response[u'main'][u'temp']
    feels_like = response[u'main'][u'feels_like']
    humidity = response[u'main'][u'humidity']
    something = response[u'weather'][0][u'description'] # What is this called? Maybe cloudliness? cloud cover? I settled for visibility which is actually the space you can see forward not what it looks like outside
    pressure = response[u'main'][u'pressure']

    print('Temperature: ' + str(temp) + ' °F')
    print('Feels like: ' + str(feels_like)+ ' °F')
    print('Humidity: ' + str(humidity))
    print("visibility: ", something)
    print('pressure: ' + str(pressure))

# Make a request for the current weather from https://api.openweathermap.org/data/2.5/weather
def get_weather(city):
    # Use an api key and a city to request from
    params = {'APPID': key, 'q': city, 'units': 'imperial'}

    response = requests.get(url, params=params)
    weather = response.json()

    name = weather[u'name']
    print("Name :", name)
    format_response(weather)

# The forcast returns the forcasted weather from 8 time slots each day for 5 days (once every 3 hours) 
# From the 40 times slots get the important information
def scrape_forecast(forcast):
    # Make a tuple containing the date and time of the weather along with the weather information for that time
    for intervals in forcast['list']:
        weather_days.append((intervals['dt_txt'], intervals))
    # Print out the weather from 3 times each day
    date = weather_days[0][0].split()[0]
    print(date)
    allowed_times = ["03:00:00", "12:00:00", "18:00:00"]
    for times in weather_days:
        new_date = times[0].split()[0]
        if new_date == date:
            if str(times[0].split()[1]) in allowed_times:
                print("\nTime: ", times[0].split()[1])
                format_response(times[1])
        else:
            date = new_date
            print("\n", date, "\n")
            if str(times[0].split()[1]) in allowed_times:
                print("Time: ", times[0].split()[1])
                format_response(times[1])

# Make a request from https://api.openweathermap.org/data/2.5/forecast
def get_forcast(city):
    params = {'APPID': key, 'q': city, 'units': 'imperial'}
    response = requests.get(forcast_url, params=params)
    forcast = response.json()
    # Scrape the response for information
    scrape_forecast(forcast)

# Some key variables
# Change the key to your api key (read README.txt)
city = input('Enter city: ')
key = ''
url = 'https://api.openweathermap.org/data/2.5/weather'
forcast_url = 'https://api.openweathermap.org/data/2.5/forecast'
weather_days = list()

# run get_weather and get_forcast
get_weather(city)
see_forcast = input(f"\nWould you like to see the 5-day forcast for {city}? ")
if see_forcast == "yes":
    get_forcast(city)
else:
    print("Oh well. Remember type 'yes' to see it.")

