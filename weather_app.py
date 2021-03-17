# https://github.com/KeithGalli/GUI

import tkinter as tk
from tkinter import font
import requests
from datetime import datetime as dt

geometry = "600x500"

# 92e299bb30a55e59e1eab96c0113dfc4 (API key)
# api.openweathermap.org/data/2.5/weather?q={city name},{country code} (url for current weather)
# api.openweathermap.org/data/2.5/forecast?q={city name},{country code} (url for 5 days forecast)
# api.openweathermap.org/data/2.5/forecast/daily?q={city name},{country code}&cnt={cnt} --> subscription required

def get_current_weather():
    weather_key = "92e299bb30a55e59e1eab96c0113dfc4"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"APPID": weather_key, "q": entry.get(), "units": "metric"}
    response = requests.get(url, params=params)
    weather = response.json()

    #print(weather)

    #label.configure(text=format_response(weather))
    label["text"] = format_current_weather(weather)


def get_forecast():
    weather_key = "92e299bb30a55e59e1eab96c0113dfc4"
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"APPID": weather_key, "q": entry.get(), "units": "metric"}
    response = requests.get(url, params=params)
    weather = response.json()

    #print(weather)
    label["text"] = format_forecast(weather)


def format_current_weather(weather):
    try:
        name = weather["name"]
        country = weather["sys"]["country"]
        desc = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]

        output = "City: %s, %s \nCondition: %s \nTemperature (°C): %s \n" % (name, country, desc, temp)
    except:
        output = "The information could not be retrieved \n Check the spelling of the city and your network connection"

    return output


def format_forecast(weather):
    
    utc_time = str(dt.utcnow()) # utc time, which is also used by the API
    date = utc_time[0:10]       # extract the date from the utc time (the second intervall statement is exclusive)
    time = utc_time[11:19]      # extract the time from the utc time
    
    try:
        
        # insert time comparison here
        #now = dt.now()
        #today12 = now.replace(hour=12, minute=0, second=0, microsecond=0)
        #now < today12        
        #now == today12
        #now > today12

        name = weather["city"]["name"]
        country = weather["city"]["country"]

        output = "City: %s, %s" %(name, country)
    except:
        output = "The information could not be retrieved"
    
    print(date, time)
    
    return output

# main window
root = tk.Tk()
root.geometry(geometry)
root.title("Weather App")

#bg_image = tk.PhotoImage(file=r"/home/simonhensel98/wallpaper.png")
#bg_label = tk.Label(root, image=bg_image)
#bg_label.place(relheight=1, relwidth=1)


frame = tk.Frame(root, bg="#80c1ff", bd=5) #bd = border
# the place function allows adjustments to the frame which remain the same upon resizing the window
# the relative parameters refer to the parent
frame.place(anchor="n", relx=0.5, rely=0.1, relheight=0.1, relwidth=0.75)

entry = tk.Entry(frame, font=("Arial", 16))
entry.insert(0, "Stuttgart, DE")
entry.place(relx=0, rely=0, relheight=1, relwidth=1)

middle_frame = tk.Frame(root, bg="#80c1ff", bd=5)
middle_frame.place(anchor="n", relx=0.5, rely=0.2, relheight=0.1, relwidth=0.75)

button = tk.Button(middle_frame, text="Get Weather", font=("Arial", 14), command=get_current_weather)
button.place(relx=0, rely=0, relheight=1, relwidth=0.45)

button2 = tk.Button(middle_frame, text="Get Forecast", font=("Arial", 14), command=get_forecast)
button2.place(relx=0.55, rely=0, relheight=1, relwidth=0.45)

lower_frame = tk.Frame(root, bg="#80c1ff", bd=5)
lower_frame.place(anchor="n", relx=0.5, rely=0.35, relheight=0.45, relwidth=0.75)

label = tk.Label(lower_frame, font=("Arial", 16), anchor="nw", bd=4, justify="left")
label.place(relx=0, rely=0, relwidth=1, relheight=1)

#print(tk.font.families())

root.mainloop()