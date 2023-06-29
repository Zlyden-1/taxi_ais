from django.urls import path

from . import views

app_name = 'references'
urlpatterns = [
    path('drivers/', views.drivers, name='drivers'),
    path('drivers/active', views.active_drivers, name='active_drivers'),
    path('driver/<int:pk>', views.DriverDetail.as_view(), name='driver'),
    path('driver/<int:pk>/delete', views.DriverDeleteView.as_view(), name='delete_driver'),
    path('driverphoto/<int:pk>/delete', views.DriverPhotoDeleteView.as_view(), name='delete_driver_photo'),
    path('drivinglicensephoto/<int:pk>/delete', views.DrivingLicenceDeleteView.as_view(),
         name='delete_driving_license_photo'),
    path('driverphoto/<int:pk>/delete', views.DriverPassportPhotoDeleteView.as_view(),
         name='delete_driver_passport_photo'),
    path('driverphoto/<int:pk>/delete', views.RentingContractPhotoDeleteView.as_view(),
         name='delete_renting_contract_photo'),
    path('driver/<int:pk>/add_photo', views.add_driver_photo, name='add_driver_photo'),
    path('driver/<int:pk>/add_passport_photo', views.add_driver_passport_photo, name='add_passport_photo'),
    path('driver/<int:pk>/add_license_photo', views.add_driving_license_photo, name='add_license_photo'),
    path('driver/<int:pk>/add_contract_photo', views.add_renting_contract_photo, name='add_contract_photo'),
    path('vehicles/', views.Vehicles.as_view(), name='vehicles'),
    path('vehicles/active', views.ActiveVehicles.as_view(), name='active_vehicles'),
    path('vehicle/<str:pk>', views.VehicleDetail.as_view(), name='vehicle'),
    path('vehicle/<str:pk>/delete', views.VehicleDeleteView.as_view(), name='delete_vehicle'),
]
