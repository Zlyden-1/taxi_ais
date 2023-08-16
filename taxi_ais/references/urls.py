from django.urls import path

from . import api_views

app_name = "references"
urlpatterns = [
    path("drivers/", api_views.DriversListAPI.as_view(), name="driver_list"),
    path(
        "drivers/options/for_vehicles",
        api_views.DriversVehicleOptionsListAPI.as_view(),
        name="driver_options_for_vehicles",
    ),
    path(
        "drivers/options/for_rents",
        api_views.DriversRentOptionsListAPI.as_view(),
        name="driver_options_for_rents",
    ),
    path("drivers/create/", api_views.CreateDriverAPI.as_view(), name="create_driver"),
    path("driver/<int:pk>/", api_views.DriverDetailAPI.as_view(), name="driver_details"),
    path("vehicles/", api_views.VehicleListAPI.as_view(), name="vehicle_list"),
    path("vehicle/<str:pk>/", api_views.VehicleDetailAPI.as_view(), name="vehicle_details"),
    path("vehicles/types/", api_views.VehicleTypeOptionsListAPI.as_view(), name="vehicle_type_list"),
    path("vehicles/locations/", api_views.VehicleLocationOptionsListAPI.as_view(), name="vehicle_location_list"),
    path("vehicles/statuses/", api_views.VehicleStatusOptionsListAPI.as_view(), name="vehicle_status_list"),
    path("vehicles/create/", api_views.VehicleCreateAPI.as_view(), name="create_vehicle"),
    path("vehicle/<str:pk>/usage_history/", api_views.VehicleHistoryListAPIView.as_view(), name="usage_history_list"),
]
