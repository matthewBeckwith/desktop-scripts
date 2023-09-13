import requests, subprocess
from datetime import datetime

# Latitude, longitude (Tampa, Florida)
LATT = 28.0763
LONG = -82.4852


class BuildWeatherReport:
    def __init__(self, latitude, longitude):
        points_url = f"https://api.weather.gov/points/{LATT},{LONG}"
        points_response = requests.get(points_url)
        points_data = points_response.json()
        location = points_data["properties"]["relativeLocation"]["properties"]

        self.city = location["city"]
        self.state = location["state"]

        forecast_url = points_data["properties"]["forecast"]
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        self.forecast = forecast_data["properties"]["periods"]

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_forecast(self):
        return self.forecast

    def get_current_weather(self):
        pass


class BuildMessage:
    def __init__(self, weather_report):
        self.city = weather_report.get_city()
        self.state = weather_report.get_state()
        self.forecast = weather_report.get_forecast()

    def get_title(self):
        return f"{self.city}, {self.state}"

    def get_content(self):
        forecast_arr = []
        forecast = ""

        for forecast in self.forecast:
            forecast_arr.append("{:<20} {:<5}\n".format(f"{forecast['name']}",f"{forecast['temperature']}{forecast['temperatureUnit']}"))
        return "".join(forecast_arr)
        


if __name__ == "__main__":
    report = BuildWeatherReport(LATT,LONG)
    message = BuildMessage(report)
    subprocess.Popen(['notify-send', message.get_title(), message.get_content()])
