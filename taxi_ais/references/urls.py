from django.urls import path

from . import views

app_name = 'contractors'
urlpatterns = [
    path('contractors/', views.contractors, name='Contractors'),
    path('add_contractor/', views.add_contractor, name='add_contractor'),
    path('contractor/<int:pk>', views.contractor_detail, name='contractor'),
    path('contractor/<int:pk>/edit', views.edit_contractor, name='edit_contractor'),
    path('contractor/<int:pk>/delete', views.delete_contractor, name='delete_contractor'),
]
