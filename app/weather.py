import requests

API_KEY = "1d9a7ef97b4aa5825ac6ae96c19e2ed3"

def get_weather(city="Lucknow"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    temp = data['main']['temp']
    humidity = data['main']['humidity']

    return temp, humidity