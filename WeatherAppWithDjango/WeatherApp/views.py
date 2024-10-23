from django.shortcuts import render, redirect
from django.views import View
from .weather_api import WeatherDataHandler
from .models import CityTemperatures
from .forms import CityForm

# Homepage
class Index(View):
    def get(self, request):
        return render(request, "WeatherApp/index.html", {"css_file":"WeatherApp/css/home.css"})

# City input page
class CityInput(View):
    # When the user lands on the page
    def get(self, request):
        return render(request, "WeatherApp/city_input.html", {"css_file":"WeatherApp/css/city_input.css",
                                                               "is_error":False})

    # When the user clicks on the button of the page
    def post(self, request):
        city_form = CityForm(request.POST)
        # If the city input is filled in
        if city_form.is_valid():
            city = request.POST.get('city')
            weather_data_handler = WeatherDataHandler(city)
            # Fetch the data from the weather API
            weather_data_handler.fetch_data()

            if weather_data_handler.response is None:
                return redirect("connection_error")

            if weather_data_handler.get_status_code() == 404:
                return render(request, "WeatherApp/city_input.html",{"css_file": "WeatherApp/css/city_input.css",
                                                                      "is_error": True})
            # Parse the data and write it to the database
            data_object = weather_data_handler.parse_data()
            weather_data_handler.write_to_db(data_object)
            # Redirect the user to the results page
            return redirect("results")

        # If the city input is left empty
        else:
            return render(request, "WeatherApp/city_input.html",{"css_file": "WeatherApp/css/city_input.css",
                                                                  "is_error": True})

# Results page
class Results(View):
    # When the user lands on the page
    def get(self, request):
        weather_objects_list = CityTemperatures.objects.all()
        return render(request, "WeatherApp/results.html", {"css_file":"WeatherApp/css/results.css",
                                                            "data": weather_objects_list})

    # If the user clicks on one of the delete buttons (recycle bin)
    def post(self, request):
        id = request.POST['id']
        CityTemperatures.objects.filter(id=id).delete()
        weather_objects_list = CityTemperatures.objects.all()
        return render(request, "WeatherApp/results.html", {"css_file":"WeatherApp/css/results.css",
                                                           "data": weather_objects_list})

# Connection error page
class ConnectionError(View):
    def get(self, request):
        return render(request, "WeatherApp/connection_error.html", {})
