import requests

city = input("Enter city name: ")


geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_response = requests.get(
    geo_url,
    params={"name": city, "count": 1}
)
geo_data = geo_response.json()

if "results" not in geo_data:
    print("City not found!")
else:
    location = geo_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    
    weather_url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code"
        }
    )

    weather = response.json()["current"]

    print("\nWeather Report for", location["name"])
    print("Temperature:", weather["temperature_2m"], "°C")
    print("Humidity:", weather["relative_humidity_2m"], "%")
    print("Weather Code:", weather["weather_code"])