from django.urls import path

from . import views


app_name = 'contractors'
urlpatterns = [
    path('contractors/', views.contractors, name='Contractors'),
    path('add_contractor/', views.add_contractor, name='add_contractor')
]
