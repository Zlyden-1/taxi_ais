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

from .models import Driver, Vehicle, VehicleLocation, VehicleStatus, VehicleType, VehicleHistory
from .serializers import (
    DriverSerializer,
    DriverDetailSerializer,
    DriverOptionsSerializer,
    VehicleSerializer,
    VehicleLocationSerializer,
    VehicleStatusSerializer,
    VehicleTypeOptionsSerializer,
    VehicleLocationOptionsSerializer,
    VehicleStatusOptionsSerializer,
    VehicleCreateUpdateSerializer,
    VehicleDetailSerializer,
    VehicleHistorySerializer,
)


class DriversListAPI(ListAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.order_by("name")


class DriversVehicleOptionsListAPI(ListAPIView):
    serializer_class = DriverOptionsSerializer
    queryset = Driver.objects.filter(vehicle=None, status=True).order_by("name")


class DriversRentOptionsListAPI(ListAPIView):
    serializer_class = DriverOptionsSerializer
    queryset = Driver.objects.exclude(vehicle=None).filter(status=True).order_by("name")


class CreateDriverAPI(CreateAPIView):
    serializer_class = DriverDetailSerializer
    queryset = Driver.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            key: value for key, value in dict(serializer.data).items() if key in DriverSerializer.Meta.fields
        }
        responce_serializer = DriverSerializer(data=response_data)
        responce_serializer.is_valid(raise_exception=True)
        return Response(responce_serializer.data, status=status.HTTP_201_CREATED)


class DriverDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = DriverDetailSerializer
    queryset = Driver.objects.all()


class VehicleListAPI(ListAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()


class VehicleLocationOptionsListAPI(ListAPIView):
    serializer_class = VehicleLocationOptionsSerializer
    queryset = VehicleLocation.objects.all()


class VehicleStatusOptionsListAPI(ListAPIView):
    serializer_class = VehicleStatusOptionsSerializer
    queryset = VehicleStatus.objects.all()


class VehicleTypeOptionsListAPI(ListAPIView):
    serializer_class = VehicleTypeOptionsSerializer
    queryset = VehicleType.objects.all()


class VehicleCreateAPI(CreateAPIView):
    serializer_class = VehicleCreateUpdateSerializer
    responce_serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        responce_serializer = self.responce_serializer_class(Vehicle.objects.get(VIN=serializer.data["VIN"]))
        return Response(responce_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        today = timezone.localdate()
        vehicle = serializer.save()
        vehicle.usage_history.add(
            vehicle.driver,
            through_defaults={
                "renting_date": today,
                "renting_end_date": None,
            },
        )


class VehicleDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleDetailSerializer
    update_serializer_class = VehicleCreateUpdateSerializer
    queryset = Vehicle.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, update=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        pk = serializer.data["VIN"]
        updated_instance = Vehicle.objects.get(pk=pk)
        update_serializer = self.get_serializer(instance)
        return Response(update_serializer.data)

    def perform_update(self, serializer):
        today = timezone.localdate()
        vehicle = serializer.save()
        last_renting = VehicleHistory.objects.filter(vehicle=vehicle).order_by("renting_date").last()
        if last_renting:
            last_renting.renting_end_date = today
        if vehicle.driver:
            vehicle.usage_history.add(
                vehicle.driver,
                through_defaults={
                    "renting_date": today,
                    "renting_end_date": None,
                },
            )

    def get_serializer(self, *args, **kwargs):
        update = kwargs.pop("update", False)
        serializer_class = self.get_serializer_class(update)
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self, update=False):
        return self.update_serializer_class if update else self.serializer_class


class VehicleHistoryListAPIView(ListAPIView):
    serializer_class = VehicleHistorySerializer
    queryset = VehicleHistory.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.filter(vehicle=self.kwargs[self.lookup_field]).order_by("-renting_date")
        return queryset
