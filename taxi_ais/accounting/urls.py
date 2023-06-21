from django.urls import path

from . import views

app_name = 'accounting'
urlpatterns = [
    path("rent_report/", views.RentReportView.as_view(), name="rent_report"),
    path("rent_list/", views.RentListView.as_view(), name="rent_list"),
]