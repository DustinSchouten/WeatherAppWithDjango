from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("city_input", views.CityInput.as_view(), name="city_input"),
    path("results", views.Results.as_view(), name="results"),
    path("connection_error", views.ConnectionError.as_view(), name="connection_error")
]