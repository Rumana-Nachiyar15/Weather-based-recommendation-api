from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"

@app.route('/weather', methods=['POST'])
def weather():
    data = request.json
    city = data['city']
    date = data['date']

    # Convert input date
    target_date = datetime.strptime(date, "%Y-%m-%d").date()

    # Forecast API
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()

    forecast_list = res['list']

    selected = None

    # Find closest date match
    for item in forecast_list:
        forecast_date = datetime.fromtimestamp(item['dt']).date()
        if forecast_date == target_date:
            selected = item
            break

    # If date not found (beyond 5 days)
    if not selected:
        selected = forecast_list[0]  # fallback

    temp = selected['main']['temp']
    condition = selected['weather'][0]['main']

    # Recommendation logic
    if "Rain" in condition:
        rec = "High chance of rain—carry an umbrella and plan indoor activities."
    elif temp > 35:
        rec = "Hot temperatures—stay hydrated and avoid long outdoor walks."
    elif temp < 20:
        rec = "Cool weather—carry light jackets."
    else:
        rec = "Expect pleasant weather—perfect for sightseeing!"

    return jsonify({"recommendation": rec})

if __name__ == '__main__':
    app.run()
