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
from .serializers import RentListSerializer


class RentListAPIView(ListAPIView):
    serializer_class = RentListSerializer
    queryset = Rent.objects.all()

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
