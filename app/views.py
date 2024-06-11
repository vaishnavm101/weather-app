from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import requests
from dotenv import load_dotenv
import os

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, CustomUserCreationForm

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@login_required
def home(request):
    load_dotenv()
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
    context = {
        "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
    }
    return render(request, "app/index.html", context)

@login_required
def get_weather(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('lat', None)
        lng = data.get('lng', None)
        if lat is None or lng is None:
            return JsonResponse({"result": False})
        load_dotenv()
        WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
        URL = f'{API_BASE_URL}?lat={lat}&lon={lng}&units=metric&appid={WEATHER_API_KEY}'
        print(URL)
        req = requests.get(URL)
        if req.status_code != 200:
            return JsonResponse({"result": False})
        response = req.json()
        context = {
            'cityName': response['name'],
            'temp': response['main']['temp'],
            'minTemp': response['main']['temp_min'],
            'maxTemp': response['main']['temp_max'],

            'humidity': response['main']['humidity'],
            'wind_deg': response['wind']['deg'],
            'temp_feels_like': response['main']['feels_like'],

            'wind_speed': response['wind']['speed'],
            'sunrise': response['sys']['sunrise'],
            'sunset': response['sys']['sunset']
        }
        return JsonResponse({"result": True, "data": context})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print("User : ", user)
            print("Logged in now...")
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    print("User is not Logged OUT")
    return redirect("home")


def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'app/register.html', {'form': form})