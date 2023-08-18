from datetime import timedelta

from django.utils import timezone
from django.db.models import QuerySet
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from .models import Rent
from .serializers import RentListSerializer, RentCreateSerializer


class RentListAPIView(ListAPIView):
    serializer_class = RentListSerializer
    queryset = Rent.objects.exclude(comment="Автоматическое начисление аренды")

    def list(self, request, *args, **kwargs):
        today = timezone.localdate()
        today_weekday = today.weekday()
        last_week_end = today - timedelta(days=today_weekday + 1)
        last_week_start = last_week_end - timedelta(days=6)
        start_date = request.query_params.get("start_date", last_week_start)
        end_date = request.query_params.get("end_date", last_week_end)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(payment_date__gte=start_date, payment_date__lte=end_date)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RentCreateAPIView(CreateAPIView):
    serializer_class = RentCreateSerializer
    queryset = Rent.objects.all()

    def create(self, request, *args, **kwargs):
        rent_data = request.data
        previous_rent = Rent.objects.filter(driver_id=rent_data["driver"]).order_by("-payment_date", "-time").first()
        if previous_rent is None:
            balance = int(rent_data["summ"])
        else:
            balance = previous_rent.balance + int(rent_data["summ"])
        rent_data["balance"] = balance
        rent_data["payment_date"] = timezone.localdate()
        rent_data["time"] = timezone.now().time()
        serializer = self.get_serializer(data=rent_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
