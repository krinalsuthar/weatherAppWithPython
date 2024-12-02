from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize window
root = Tk()
root.title("Weather App")
root.geometry("450x700")
root.configure(bg="#E8E8E8")  # Light background color

# Rounded Rectangle Function
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Draw a rounded rectangle on the canvas."""
    points = [
        x1 + radius, y1,  # Top-left
        x2 - radius, y1,  # Top-right
        x2 - radius, y1, x2, y1,  # Curve
        x2, y1 + radius,  # Right-side
        x2, y2 - radius,  # Bottom-right
        x2, y2 - radius, x2, y2,  # Curve
        x2 - radius, y2,  # Bottom side
        x1 + radius, y2,  # Bottom-left
        x1 + radius, y2, x1, y2,  # Curve
        x1, y2 - radius,  # Left-side
        x1, y1 + radius,  # Top-left
        x1, y1 + radius, x1, y1,  # Curve
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Stylish Fonts
title_font = ("Helvetica", 20, "bold")
label_font = ("Helvetica", 15)
data_font = ("Helvetica", 15, "italic")

# Header
header = Label(root, text="Weather App", font=title_font, bg='#E8E8E8', fg='#333')
header.pack(pady=20)

# Date
current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
date_label = Label(root, text=current_date, font=("Helvetica", 15), bg="#E8E8E8", fg="#333")
date_label.pack(pady=10)

# City Entry
city_name = StringVar()
city_entry = ttk.Entry(root, textvariable=city_name, font=label_font, justify='center')
city_entry.pack(pady=10, ipady=5)

# Search Button
def fetch_weather():
    city = city_name.get()  # Get city from user input
    api_key = os.getenv('api_key')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            # Update card content
            temp_label.config(text=f"{temp} °C")
            humidity_label.config(text=f"Humidity: {humidity} %")
            wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
            city_label.config(text=f"{city.title()}")
        else:
            temp_label.config(text="--")
            humidity_label.config(text="Error: City not found.")
            wind_label.config(text="--")
            city_label.config(text="")
    except Exception as e:
        temp_label.config(text="Error")
        humidity_label.config(text=str(e))

search_button = ttk.Button(root, text="Search", command=fetch_weather)
search_button.pack(pady=10)

# Canvas for Rounded Card
canvas = Canvas(root, width=300, height=250, bg="#E8E8E8", highlightthickness=0)
canvas.pack(pady=20)

# Create the rounded rectangle (card)
create_rounded_rectangle(canvas, 10, 10, 290, 240, radius=30, fill="white", outline="#CCCCCC")

# Add Labels inside the card
city_label = Label(canvas, text="City Name", font=label_font, bg="white", fg="#333")
canvas.create_window(150, 40, window=city_label)

temp_label = Label(canvas, text="-- °C", font=("Helvetica", 50), bg="white", fg="#FF5733")
canvas.create_window(150, 100, window=temp_label)

humidity_label = Label(canvas, text="Humidity: --", font=data_font, bg="white")
canvas.create_window(150, 150, window=humidity_label)

wind_label = Label(canvas, text="Wind Speed: --", font=data_font, bg="white")
canvas.create_window(150, 190, window=wind_label)

# Footer
footer = Label(root, text="All temperatures in Celsius", font=("italic", 10), bg="#E8E8E8")
footer.pack(side=BOTTOM, pady=10)

root.mainloop()
