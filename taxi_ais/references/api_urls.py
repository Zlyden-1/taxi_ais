from django.urls import path

from . import api_views

app_name = 'api_references'
urlpatterns = [
    path('drivers/', api_views.DriversListAPI.as_view(), name='drivers'),
]