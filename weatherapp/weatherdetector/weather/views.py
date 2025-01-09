from django.shortcuts import render
import json
from urllib.request import urlopen

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        # Option 1: Add units=metric to get Celsius directly from API
        res = urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=b9e9e1213c7a69763159b896936c650f')
        json_string = res.read().decode('utf-8')
        json_data = json.loads(json_string)
        
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(json_data['coord']['lon']) + ' ' +
            str(json_data['coord']['lat']),
            "temp": f"{json_data['main']['temp']}°C",  # Temperature will already be in Celsius
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
        }
        
    else:
        city = ''
        data = {}
    return render(request, 'index.html', {'city': city, 'data': data})