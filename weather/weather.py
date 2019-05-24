import tkinter as tk
import requests
import math
from tkinter import font
from PIL import Image, ImageTk
root = tk.Tk()
 
HEIGHT = 500
WIDTH = 600

def test_function(entry):
    print("this is the entry:", entry)
#e869269176dd7bce8b0d1cf4c50b95dc
#api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}
# api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
def format_response(weather):
    try:
        name = weather['city']['name']
        description = weather['list'][0]['weather'][0]['description']
        special = weather['list'][0]['weather'][0]['main']
        temp = weather['list'][0]['main']['temp']
        temp = (temp-32)*0.5556
        temp = math.floor(temp)
        final_str = 'City: %s \nConditions: %s\nSpecial: %s \nTemperature (°C): %s' % (name, description, special, temp)
        # final_str = str(name) + '' + str(description) + '' + str(special) + '' + str(temp)
    except:
        final_str = 'There was a problem retrieving that information'
    return final_str
def get_weather(city):
    weather_key = 'e869269176dd7bce8b0d1cf4c50b95dc' 
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {'APPID' : weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params=params)
    # print(response.json())
    weather = response.json()
    # print(weather['city']['name'])
    # print(weather['list'][0]['weather'][0]['description'])
    # print(weather['list'][0]['weather'][0]['main'])
    # print(weather['list'][0]['main']['temp'])

    label['text'] = format_response(weather)
    icon_name = weather['list'][0]['weather'][0]['icon']
    open_image(icon_name)
    # print(photo)
def open_image(icon):
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw', image=img)
    weather_icon.image = img


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

backgound_image = tk.PhotoImage(file='download.png')
backgound_label = tk.Label(root, image=backgound_image)
backgound_label.place(relwidth=1,relheight=1)

frame = tk.Frame(root,bg='#80c1ff', bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor='n')

entry = tk.Entry(frame, font=('Cuorier',18))
entry.place( relwidth=0.65,relheight=1) 

button = tk.Button(frame, text="Get Weather", font=('Cuorier',12), command=lambda: get_weather(entry.get()))
button.place(relx=0.7,relwidth=0.3,relheight=1)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font=('Cuorier',18),anchor='nw', justify='left',bd=4)
# label.pack(side='left', fill='both')
# label.grid(row=0, column=1)

label.place(relwidth=1,relheight=1)
weather_icon = tk.Canvas(label, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)




root.mainloop()