from django.utils import timezone

from rest_framework import serializers

from references.models import Driver

from .models import Rent


class DriverSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="__str__")

    class Meta:
        model = Driver
        fields = ["id", "name"]


class RentListSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = Rent
        fields = ["driver", "payment_date", "summ"]


class RentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = "__all__"


class BalanceListSerializer(serializers.Serializer):
    driver = DriverSerializer()
    balance = serializers.FloatField()
