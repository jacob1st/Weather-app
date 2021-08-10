# The request library allows us to make GET requests to the weather api
import requests
# The tkinter library is used for the gui
import tkinter as tk

# get some important weather information from the dictionary or list provided from the response
def format_response(response):
    temp = response[u'main'][u'temp']
    feels_like = response[u'main'][u'feels_like']
    humidity = response[u'main'][u'humidity']
    something = response[u'weather'][0][u'description'] # What is this called? Maybe cloudliness? cloud cover? I settled for visibility which is actually the space you can see forward not what it looks like outside
    pressure = response[u'main'][u'pressure']

    weather_label['text'] += f'Temperature: {str(temp)} °F \n'
    weather_label['text'] += f'Feels like: {str(feels_like)} °F \n'
    weather_label['text'] += f'Humidity: {str(humidity)}\n'
    weather_label['text'] += f'visibility: {str(something)}\n'
    weather_label['text'] += f'pressure: {str(pressure)}\n'

# same as format_response, but it doesn't print the info it saves it in a string to later put in a list to view
def format_forcast(response, today):
    temp = response[u'main'][u'temp']
    feels_like = response[u'main'][u'feels_like']
    humidity = response[u'main'][u'humidity']
    something = response[u'weather'][0][u'description'] # What is this called? Maybe cloudliness? cloud cover? I settled for visibility which is actually the space you can see forward not what it looks like outside
    pressure = response[u'main'][u'pressure']

    today += "Temperature: " + str(temp) + '\n'
    today += "Feels_like: " + str(feels_like) + '\n'
    today += "Humidity: " + str(humidity) + '\n'
    today += "Visibility: " + str(something) + '\n'
    today += "Pressure: " + str(pressure) + '\n'

    return today
# Make a request for the current weather from https://api.openweathermap.org/data/2.5/weather
def get_weather(city):
    # Use an api key and a city to request from
    params = {'APPID': key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        weather_label['text'] = "Something went wrong. Please try again. \nStatus Code: " + str(response.status_code)
        return
    weather = response.json()

    # reset the gui windows text fonr and print the city name
    weather_label['font'] = 'Arial 20'
    name = weather[u'name']
    weather_label['text'] = f'Name : {name}\n'
    format_response(weather)
    # place the button to view the forcast and make the request to receive the forcast now
    next_button.place(relheight=.05, relwidth=.4, relx=.2, rely=.92)
    # reset any lists in between requests
    full_forcast.clear()
    weather_days.clear()
    get_forcast(city)

# The forcast returns the forcasted weather from 8 time slots each day for 5 days (once every 3 hours) 
# From the 40 times slots get the important information
def scrape_forecast(forcast):
    # Make a tuple containing the date and time of the weather along with the weather information for that time
    for intervals in forcast['list']:
        weather_days.append((intervals['dt_txt'], intervals))
    # Print out the weather from 3 times each day
    date = weather_days[0][0].split()[0] # Save the current date
    todays_weather_forcast = "\n" + str(date)
    allowed_times = ["03:00:00", "12:00:00", "18:00:00"] # The times that information will be returned from (we dont want every 3 hours)
    count = 0
    for times in weather_days:
        if count == 3: # Keep track of the different days
            full_forcast.append(todays_weather_forcast) # put the days information in a global list and reset the string
            todays_weather_forcast = ""
            count = 0
        new_date = times[0].split()[0]
        if new_date == date:
            if str(times[0].split()[1]) in allowed_times: # Take that time's information and format it
                todays_weather_forcast += '\nTime: ' + str(times[0].split()[1]) + '\n'
                todays_weather_forcast = format_forcast(times[1], todays_weather_forcast)
                count += 1
        else:
            date = new_date
            todays_weather_forcast += '\n' + str(date) + '\n'
            if str(times[0].split()[1]) in allowed_times:
                todays_weather_forcast += 'Time: ' + str(times[0].split()[1]) + '\n'
                todays_weather_forcast = format_forcast(times[1], todays_weather_forcast)
                count += 1
    # full_forcast.append("There are no more forcasts available past that date")
# Make a request from https://api.openweathermap.org/data/2.5/forecast
def get_forcast(city):

    params = {'APPID': key, 'q': city, 'units': 'imperial'}
    response = requests.get(forcast_url, params=params)
    forcast = response.json()
    # Scrape the response for information
    scrape_forecast(forcast)

# One by one view the information saved in the full_forcast list
def tom_forcast():
    if len(full_forcast) == 1:
        full_forcast.append("There are no more forcasts available past that date")
    weather_label['font'] = 'Arial 12'
    weather_label['text'] = full_forcast[0]
    full_forcast.pop(0) # Remove the string from the list so we can view the next one 

# Some key variables
# Change the key to your api key (read README.txt)
key = ''
url = 'https://api.openweathermap.org/data/2.5/weather'
forcast_url = 'https://api.openweathermap.org/data/2.5/forecast'
weather_days = list()
full_forcast = list()

# The GUI
root = tk.Tk()

root.title("Weather App")
root.geometry("900x700")

# The Canvas (background)
canvas = tk.Canvas(root, bg="blue")
canvas.place(relheight=1, relwidth=1, relx=0, rely=0)

# The text box to enter the city
entry = tk.Entry(canvas)
entry.place(relheight=.05, relwidth=.8, relx=.08, rely=.05)

# A little tag for the entry
label = tk.Label(canvas, bg="blue", font="Arial 11", text="City: ", fg="white")
label.place(relheight=.05, relwidth=.05, relx=.03, rely=.05)

# The Button to submit the city name and get the weather (runs get_weather())
button = tk.Button(canvas, text="Get Weather!", font="Arial 11", bg="white", command=lambda: get_weather(entry.get()))
button.place(relheight=.05, relwidth=.1, relx=.89, rely=.05)

# Defines the button to view tommorrow's forcast but we dont place it yet (place it after we get the weather)
next_button = tk.Button(canvas, text="View tommorrow's forcast", font="Arial 12", command=lambda: tom_forcast())

# This si where we print out all the information
weather_label = tk.Label(canvas, text="Input city/city area code/or \nlatitude and longitude to get weather", bg="white", font="Arial 20")
weather_label.place(relheight=.7, relwidth=.8, relx=.1, rely=.2)

root.mainloop()