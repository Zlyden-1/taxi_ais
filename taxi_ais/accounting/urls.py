from django.urls import path

from . import api_views

app_name = "accounting"
urlpatterns = [
    path("rents/", api_views.RentListAPIView.as_view(), name="rent_list"),
]
