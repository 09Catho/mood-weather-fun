from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="Weather Mood Synthesizer API")
templates = Jinja2Templates(directory="templates")

OPENWEATHER_API_KEY = "f0a7f045e24b48b52757a5618184db3c"

def synthesize_mood(weather_desc: str, temp_c: float):
    if 'rain' in weather_desc.lower():
        return "Perfect for introspection, Netflix, and hot chai."
    elif 'clear' in weather_desc.lower():
        if temp_c > 28:
            return "Sunny and blazing—grab your shades, hydrate, and conquer the day!"
        else:
            return "Clear skies! Best for adventures, productivity, or rooftop parties."
    elif 'cloud' in weather_desc.lower():
        return "Cloudy with a chance of deep thoughts and lo-fi beats."
    elif 'snow' in weather_desc.lower():
        return "Snowy wonderland—build a snowman or cozy up with a book."
    elif 'storm' in weather_desc.lower() or 'thunder' in weather_desc.lower():
        return "Epic storm brewing! Maybe stay indoors and plot your next move."
    else:
        return "Unique weather—embrace the unpredictability!"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/mood")
def get_weather_mood(city: str = Query(..., description="Your city name")):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + OPENWEATHER_API_KEY + "&units=metric"
    resp = requests.get(url)
    if resp.status_code != 200:
        return JSONResponse(status_code=404, content={"error": "City not found or weather API error."})

    data = resp.json()
    weather_desc = data['weather'][0]['description']
    temp_c = data['main']['temp']

    mood = synthesize_mood(weather_desc, temp_c)

    return {
        "city": city.title(),
        "weather": weather_desc,
        "temperature_celsius": temp_c,
        "mood_report": mood
    }
