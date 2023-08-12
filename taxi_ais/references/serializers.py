from rest_framework import serializers

from .models import Driver, Vehicle, VehicleLocation, VehicleType, VehicleStatus


class DriverSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Driver
        fields = ["id", "second_name", "first_name", "patronimic", "name", "status"]


class DriverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class ShortVehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ["brand", "model"]


class GenericVehicleOptionsSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source="id")
    name = serializers.CharField(source="__str__")


class VehicleTypeOptionsSerializer(GenericVehicleOptionsSerializer):
    class Meta:
        model = VehicleType
        fields = ["value", "name"]


class VehicleStatusOptionsSerializer(GenericVehicleOptionsSerializer):
    class Meta:
        model = VehicleStatus
        fields = ["value", "name"]


class VehicleLocationOptionsSerializer(GenericVehicleOptionsSerializer):
    class Meta:
        model = VehicleLocation
        fields = ["value", "name"]


class DriverOptionsSerializer(GenericVehicleOptionsSerializer):
    class Meta:
        model = Driver
        fields = ["value", "name"]


class VehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStatus
        fields = "__all__"


class VehicleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleLocation
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_type = ShortVehicleTypeSerializer()
    location = VehicleLocationSerializer()
    status = VehicleStatusSerializer()
    driver = DriverSerializer()

    class Meta:
        model = Vehicle
        fields = ["VIN", "license_plate", "vehicle_type", "status", "driver", "location"]


class VehicleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ("usage_history",)


class VehicleDetailSerializer(serializers.ModelSerializer):
    vehicle_type = VehicleTypeOptionsSerializer()
    status = VehicleStatusOptionsSerializer()
    location = VehicleLocationOptionsSerializer()
    driver = DriverOptionsSerializer()

    class Meta:
        model = Vehicle
        exclude = [
            "registration_certificate_scan",
            "vehicle_passport_scan",
            "acceptance_certificate_scan",
            "leasing_contract_scan",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
