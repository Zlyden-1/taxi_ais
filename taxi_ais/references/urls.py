from django.urls import path

from . import views

app_name = 'contractors'
urlpatterns = [
    path('contractors/', views.contractors, name='Contractors'),
    path('add_contractor/', views.add_contractor, name='add_contractor'),
    path('contractor/<int:pk>', views.contractor_detail, name='contractor'),
    path('contractor/<int:pk>/edit', views.edit_contractor, name='edit_contractor'),
    path('contractor/<int:pk>/delete', views.delete_contractor, name='delete_contractor'),
    path('drivers/', views.drivers, name='drivers'),
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
]
