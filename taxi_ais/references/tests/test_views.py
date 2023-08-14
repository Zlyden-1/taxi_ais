from datetime import date
from collections import OrderedDict
from copy import deepcopy

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from ..models import Driver, Vehicle, VehicleLocation, VehicleStatus, VehicleType, VehicleHistory
from ..serializers import DriverDetailSerializer, VehicleDetailSerializer


class DriverListAPITests(APITestCase):
    test_driver_data = {
        "second_name": "dcvftn",
        "first_name": "cdcvfgbhnj",
        "patronimic": "cdfbhnjk",
        "name": "dvfgnj,",
        "citizenship": "",
        "passport_id": "",
        "passport_issue_date": date(1900, 1, 1),
        "date_of_birth": date(1900, 1, 1),
        "place_of_birth": "",
        "residence_place": "",
        "phone_number": "123456",
        "driving_license_id": "swvb",
        "driving_license_category": "fvgbg",
        "driving_license_validity_period": "2023-07-15",
        "deposit": 11111,
        "status": True,
        "comment": "aaaaaa",
        "telegram_id": "@dghh",
    }

    def test_create_driver_response_data(self):
        response = self.client.post("/api/references/drivers/create/", self.test_driver_data, format="json")
        self.assertEquals(
            response.data,
            {
                "id": 1,
                "second_name": "dcvftn",
                "first_name": "cdcvfgbhnj",
                "patronimic": "cdfbhnjk",
                "name": "dvfgnj,",
                "status": True,
            },
        )

    def test_create_driver_db(self):
        response = self.client.post("/api/references/drivers/create/", self.test_driver_data, format="json")
        self.assertEquals(Driver.objects.all().count(), 1)


class DetailDriverAPITests(APITestCase):
    def setUp(self):
        Driver.objects.create(
            second_name="dcvftn",
            first_name="cdcvfgbhnj",
            patronimic="cdfbhnjk",
            name="dvfgnj,",
            citizenship="",
            passport_id="",
            passport_issue_date=date(1900, 1, 1),
            date_of_birth=date(1900, 1, 1),
            place_of_birth="",
            residence_place="",
            phone_number="123456",
            driving_license_id="swvb",
            driving_license_category="fvgbg",
            driving_license_validity_period="2023-07-15",
            deposit=11111,
            status=True,
            comment="aaaaaa",
            telegram_id="@dghh",
        )

    def test_retrieve_details(self):
        response = self.client.get("/api/references/driver/1/")
        self.assertEquals(response.data, DriverDetailSerializer(Driver.objects.get(pk=1)).data)

    def test_patch_driver(self):
        response = self.client.patch("/api/references/driver/1/", {"citizenship": "Russia"}, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            DriverDetailSerializer(Driver.objects.get(pk=1)).data,
            DriverDetailSerializer(
                {
                    "id": 1,
                    "second_name": "dcvftn",
                    "first_name": "cdcvfgbhnj",
                    "patronimic": "cdfbhnjk",
                    "name": "dvfgnj,",
                    "citizenship": "Russia",
                    "passport_id": "",
                    "passport_issue_date": date(1900, 1, 1),
                    "date_of_birth": date(1900, 1, 1),
                    "place_of_birth": "",
                    "residence_place": "",
                    "phone_number": "123456",
                    "driving_license_id": "swvb",
                    "driving_license_category": "fvgbg",
                    "driving_license_validity_period": "2023-07-15",
                    "deposit": 11111,
                    "status": True,
                    "comment": "aaaaaa",
                    "telegram_id": "@dghh",
                },
            ).data,
        )

    def test_deletion(self):
        response = self.client.delete("/api/references/driver/1/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class VehicleListAPITest(APITestCase):
    vehicle_response_data = [
        OrderedDict(
            {
                "VIN": "пгплршрш",
                "license_plate": "рлоилишг",
                "vehicle_type": OrderedDict([("brand", "RENAULT"), ("model", "LOGAN")]),
                "status": OrderedDict([("id", 1), ("name", "Активно"), ("is_active", True)]),
                "driver": OrderedDict(
                    [
                        ("id", 1),
                        ("second_name", None),
                        ("first_name", None),
                        ("patronimic", None),
                        ("name", "ewfehjy"),
                        ("status", True),
                    ]
                ),
                "location": OrderedDict([("id", 1), ("place", "Самара")]),
            }
        )
    ]

    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        type_ = VehicleType.objects.create(
            brand="RENAULT", model="LOGAN", vehicle_type="jdcdjc", manufacturer="ldncd", rent_price=1000
        )
        status = VehicleStatus.objects.create(name="Активно", is_active=True)
        location = VehicleLocation(place="Самара")
        for i in driver, type_, status, location:
            i.save()
        Vehicle.objects.create(
            VIN="пгплршрш",
            license_plate="рлоилишг",
            vehicle_type=type_,
            status=status,
            driver=driver,
            location=location,
        )

    def test_retrieve_vehicle_list(self):
        response = self.client.get("/api/references/vehicles/")
        self.assertEquals(response.data, self.vehicle_response_data)


class VehicleCreateAPITest(APITestCase):
    test_vehicle_data = OrderedDict(
        {
            "VIN": "пгплршрш",
            "license_plate": "рлоилишг",
            "vehicle_type": 1,
            "status": 1,
            "driver": 1,
            "location": 1,
        }
    )
    response_data = OrderedDict(
        {
            "VIN": "пгплршрш",
            "license_plate": "рлоилишг",
            "vehicle_type": OrderedDict([("brand", "RENAULT"), ("model", "LOGAN")]),
            "status": OrderedDict([("id", 1), ("name", "Активно"), ("is_active", True)]),
            "driver": OrderedDict(
                [
                    ("id", 1),
                    ("second_name", None),
                    ("first_name", None),
                    ("patronimic", None),
                    ("name", "ewfehjy"),
                    ("status", True),
                ]
            ),
            "location": OrderedDict([("id", 1), ("place", "Самара")]),
        }
    )

    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        type_ = VehicleType.objects.create(
            brand="RENAULT", model="LOGAN", vehicle_type="jdcdjc", manufacturer="ldncd", rent_price=1000
        )
        status = VehicleStatus.objects.create(name="Активно", is_active=True)
        location = VehicleLocation(place="Самара")
        for i in driver, type_, status, location:
            i.save()

    def test_creation(self):
        response = self.client.post("/api/references/vehicles/create/", self.test_vehicle_data, format="json")
        self.assertEquals(response.data, self.response_data)

    def test_history(self):
        self.client.post("/api/references/vehicles/create/", self.test_vehicle_data, format="json")
        self.assertEquals(len(Vehicle.objects.all()[0].usage_history.all()), 1)


class VehicleOptionsAPITest(APITestCase):
    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        type_ = VehicleType.objects.create(
            brand="RENAULT", model="LOGAN", vehicle_type="jdcdjc", manufacturer="ldncd", rent_price=1000
        )
        status = VehicleStatus.objects.create(name="Активно", is_active=True)
        location = VehicleLocation(place="Самара")
        for i in driver, type_, status, location:
            i.save()

    def test_retrieve_vehicle_type_list(self):
        response = self.client.get("/api/references/vehicles/types/")
        self.assertEquals(response.data, [OrderedDict([("value", 1), ("name", "RENAULT LOGAN")])])

    def test_retrieve_vehicle_status_list(self):
        response = self.client.get("/api/references/vehicles/statuses/")
        self.assertEquals(response.data, [OrderedDict([("value", 1), ("name", "Активно")])])

    def test_retrieve_vehicle_location_list(self):
        response = self.client.get("/api/references/vehicles/locations/")
        self.assertEquals(response.data, [OrderedDict([("value", 1), ("name", "Самара")])])

    def test_retrieve_driver_options_list(self):
        response = self.client.get("/api/references/drivers/options/")
        self.assertEquals(response.data, [OrderedDict([("value", 1), ("name", "ewfehjy")])])


class VehicleDetailAPITests(APITestCase):
    vehicle_data = {
        "VIN": "11",
        "vehicle_type": None,
        "status": None,
        "location": None,
        "driver": None,
        "license_plate": "11",
        "registration_certificate_id": "11",
        "vehicle_passport_id": "11",
        "engine_id": "11",
        "color": "11",
        "leasing_contract_id": "111",
        "insurance_policy_series": "111",
        "insurance_policy_id": "11",
        "leasing_contract_date": "2023-08-01",
        "lessor": "1111",
        "manufacture_year": 11111,
        "rent_type": "А",
    }
    responce_data = {
        "VIN": "11",
        "vehicle_type": OrderedDict([("value", 1), ("name", "RENAULT LOGAN")]),
        "status": OrderedDict([("value", 1), ("name", "Активно")]),
        "location": OrderedDict([("value", 1), ("name", "Самара")]),
        "driver": OrderedDict([("value", 1), ("name", "ewfehjy")]),
        "license_plate": "11",
        "registration_certificate_id": "11",
        "vehicle_passport_id": "11",
        "engine_id": "11",
        "color": "11",
        "leasing_contract_id": "111",
        "insurance_policy_series": "111",
        "insurance_policy_id": "11",
        "leasing_contract_date": "2023-08-01",
        "lessor": "1111",
        "manufacture_year": 11111,
        "rent_type": "А",
    }

    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        other_driver = Driver.objects.create(name="other", status=True)
        type_ = VehicleType.objects.create(
            brand="RENAULT", model="LOGAN", vehicle_type="jdcdjc", manufacturer="ldncd", rent_price=1000
        )
        status = VehicleStatus.objects.create(name="Активно", is_active=True)
        location = VehicleLocation(place="Самара")
        for i in driver, type_, status, location:
            i.save()
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        vehicle.vehicle_type = type_
        vehicle.status = status
        vehicle.location = location
        vehicle.driver = driver
        vehicle.save()

    def test_retrieve_details(self):
        response = self.client.get("/api/references/vehicle/11/")
        self.assertEquals(response.data, self.responce_data)

    def test_patch_vehicle(self):
        self.assertEquals(len(Vehicle.objects.first().usage_history.all()), 0)
        responce_data = deepcopy(self.responce_data)
        responce_data["driver"] = OrderedDict([("value", 2), ("name", "other")])
        response = self.client.patch("/api/references/vehicle/11/", {"driver": 2}, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, responce_data)
        self.assertEquals(len(Vehicle.objects.first().usage_history.all()), 1)

    def test_deletion(self):
        response = self.client.delete("/api/references/driver/1/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class VehicleHistoryListAPITests(APITestCase):
    vehicle_data = {
        "VIN": "11",
        "vehicle_type": None,
        "status": None,
        "location": None,
        "driver": None,
        "license_plate": "11",
        "registration_certificate_id": "11",
        "vehicle_passport_id": "11",
        "engine_id": "11",
        "color": "11",
        "leasing_contract_id": "111",
        "insurance_policy_series": "111",
        "insurance_policy_id": "11",
        "leasing_contract_date": "2023-08-01",
        "lessor": "1111",
        "manufacture_year": 11111,
        "rent_type": "А",
    }
    responce_data = [
        OrderedDict([("id", 2), ("name", "ewfehjy LOGAN 11 с 2023-08-14 по сегодня")]),
        OrderedDict([("id", 1), ("name", "other LOGAN 11 с 2000-01-01 по 2023-08-14")]),
    ]

    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        other_driver = Driver.objects.create(name="other", status=True)
        type_ = VehicleType.objects.create(
            brand="RENAULT", model="LOGAN", vehicle_type="jdcdjc", manufacturer="ldncd", rent_price=1000
        )
        status = VehicleStatus.objects.create(name="Активно", is_active=True)
        location = VehicleLocation(place="Самара")
        for i in driver, type_, status, location:
            i.save()
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        vehicle.vehicle_type = type_
        vehicle.status = status
        vehicle.location = location
        vehicle.driver = driver
        vehicle.save()
        vehicle.usage_history.add(
            other_driver,
            through_defaults={
                "renting_date": date(2000, 1, 1),
                "renting_end_date": date.today(),
            },
        )
        vehicle.usage_history.add(
            driver,
            through_defaults={
                "renting_date": date.today(),
                "renting_end_date": None,
            },
        )

    def test_retrieve_history(self):
        response = self.client.get("/api/references/vehicle/11/usage_history/")
        self.assertEquals(response.data, self.responce_data)
