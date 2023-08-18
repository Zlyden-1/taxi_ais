from django.urls import path

from . import api_views

app_name = "accounting"
urlpatterns = [
    path("rents/", api_views.RentListAPIView.as_view(), name="rent_list"),
    path("rent/create/", api_views.RentCreateAPIView.as_view(), name="create_rent"),
]
