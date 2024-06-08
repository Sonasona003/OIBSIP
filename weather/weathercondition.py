import requests
import tkinter as tk
from tkinter import messagebox

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")
        self.master.geometry("400x300")

        self.api_key = "39"

        self.label = tk.Label(master, text="hyderabad:")
        self.label.pack(pady=10)

        self.location_entry = tk.Entry(master)
        self.location_entry.pack(pady=5)
        self.location_entry.insert(0, "500044")  # Example ZIP code

        self.get_weather_button = tk.Button(master, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack(pady=5)

        self.weather_info = tk.Label(master, text="")
        self.weather_info.pack(pady=10)

    def get_weather(self):
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a city or ZIP code.")
            return

        url = f"http://maps.openweathermap.org/maps/2.0/weather"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                messagebox.showerror("Error", f"City or ZIP code '{location}' not found.")
            elif response.status_code == 401:
                messagebox.showerror("Error", "Invalid API key. Please provide a valid API key.")
            else:
                messagebox.showerror("Error", f"HTTP error occurred: {http_err}")
        except Exception as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
        else:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]

            temperature = main['temp']
            humidity = main['humidity']
            description = weather['description']

            weather_data = (f"Weather in {location}:\n"
                            f"Temperature: {temperature}°C\n"
                            f"Humidity: {humidity}%\n"
                            f"Conditions: {description}")

            self.weather_info.config(text=weather_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
