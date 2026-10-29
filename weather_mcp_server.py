import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather MCP Tool")


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current temperature, humidity, and weather code for a city."""
    try:
        # Find the city's latitude and longitude.
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"City not found: {city}"

        location = geo_data["results"][0]

        # Get the current weather for those coordinates.
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        current = weather_response.json()["current"]

        return (
            f"Weather for {location['name']}:\n"
            f"Temperature: {current['temperature_2m']} °C\n"
            f"Humidity: {current['relative_humidity_2m']}%\n"
            f"Weather code: {current['weather_code']}"
        )
    except requests.RequestException as error:
        return f"Could not get weather right now: {error}"


if __name__ == "__main__":
    mcp.run()
