from django.urls import path

from . import views

app_name = 'contractors'
urlpatterns = [
    path('', views.index, name='index'),
    path('references/contractors/', views.contractors, name='Contractors'),
    path('references/add_contractor/', views.add_contractor, name='add_contractor'),
    path('references/contractor/<int:pk>', views.contractor_detail, name='contractor'),
    path('references/contractor/<int:pk>/edit', views.edit_contractor, name='edit_contractor'),
    path('references/contractor/<int:pk>/delete', views.delete_contractor, name='delete_contractor'),
    path('references/drivers/', views.drivers, name='drivers'),
    path('references/drivers/active', views.active_drivers, name='active_drivers'),
    path('references/driver/<int:pk>', views.DriverDetail.as_view(), name='driver'),
    path('references/driver/<int:pk>/delete', views.DriverDeleteView.as_view(), name='delete_driver'),
    path('references/driverphoto/<int:pk>/delete', views.DriverPhotoDeleteView.as_view(), name='delete_driver_photo'),
    path('references/drivinglicensephoto/<int:pk>/delete', views.DrivingLicenceDeleteView.as_view(),
         name='delete_driving_license_photo'),
    path('references/driverphoto/<int:pk>/delete', views.DriverPassportPhotoDeleteView.as_view(),
         name='delete_driver_passport_photo'),
    path('references/driverphoto/<int:pk>/delete', views.RentingContractPhotoDeleteView.as_view(),
         name='delete_renting_contract_photo'),
    path('references/driver/<int:pk>/add_photo', views.add_driver_photo, name='add_driver_photo'),
    path('references/driver/<int:pk>/add_passport_photo', views.add_driver_passport_photo, name='add_passport_photo'),
    path('references/driver/<int:pk>/add_license_photo', views.add_driving_license_photo, name='add_license_photo'),
    path('references/driver/<int:pk>/add_contract_photo', views.add_renting_contract_photo, name='add_contract_photo'),
    path('references/vehicles/', views.Vehicles.as_view(), name='vehicles'),
    path('references/vehicles/active', views.ActiveVehicles.as_view(), name='active_vehicles'),
    path('references/vehicle/<str:pk>', views.VehicleDetail.as_view(), name='vehicle'),
    path('references/vehicle/<str:pk>/delete', views.VehicleDeleteView.as_view(), name='delete_vehicle'),
]
