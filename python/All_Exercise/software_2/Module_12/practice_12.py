# Task 1


import requests,json

request = "https://api.chucknorris.io/jokes/random"
response = requests.get(request).json()
# print(json.dumps(response, indent=2))
print(response["value"])
# print(response.status_code)




# Task 2


import requests

API_KEY = "e0ab9f5b031f0663da10031fd4e86adc"


city = input("Enter municipality: ")

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(url, params=params)
data = response.json()

if str(data.get("cod")) == "200":
    description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]

    print(f"Weather: {description}")
    print(f"Temperature: {temperature:.1f} °C")
else:
    print(f"Error: {data.get('message', 'Unknown error')}")