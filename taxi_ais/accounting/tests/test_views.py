from datetime import date, time
from collections import OrderedDict
from copy import deepcopy

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from references.models import Driver

from ..models import Rent
from ..serializers import RentListSerializer


class RentListAPITest(APITestCase):
    list_all_responce_data = [
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2022-01-01"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2022-02-01"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2023-01-01"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2023-07-01"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2023-07-10"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2023-08-12"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2023-08-13"),
                ("summ", 1000.0),
            ]
        ),
        OrderedDict(
            [
                ("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])),
                ("payment_date", "2023-08-15"),
                ("summ", 1000.0),
            ]
        ),
    ]

    balance_all_data = [OrderedDict([("driver", OrderedDict([("id", 1), ("name", "ewfehjy")])), ("balance", 7000.0)])]

    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        summ = 1000
        dates = (
            date(2022, 1, 1),
            date(2022, 2, 1),
            date(2023, 1, 1),
            date(2023, 7, 1),
            date(2023, 7, 10),
            date(2023, 8, 12),
            date(2023, 8, 13),
            date(2023, 8, 15),
        )
        for n, i in enumerate(dates):
            Rent.objects.create(driver=driver, summ=summ, payment_date=i, balance=n * summ)

    def test_rent_list_all(self):
        response = self.client.get(f"/api/accounting/rents/?start_date=2022-1-1&&end_date=2024-1-1")
        self.assertEquals(response.data, self.list_all_responce_data)

    def test_balance_list_all(self):
        response = self.client.get(f"/api/accounting/rents/balances/?start_date=2022-1-1&&end_date=2024-1-1")
        self.assertEquals(response.data, self.balance_all_data)

    # def test_list_for_last_week(self):
    #     response = self.client.get(f"/api/accounting/rents/")
    #     self.assertEquals(response.data, self.list_all_responce_data)


class RentCreateAPITest(APITestCase):
    first_rent_data = OrderedDict(
        {
            "driver": 2,
            "summ": 1000,
            "comment": "first",
        }
    )
    next_rent_data = OrderedDict(
        {
            "driver": 1,
            "summ": 1000,
            "comment": "second",
        }
    )

    def setUp(self):
        driver = Driver.objects.create(name="ewfehjy", status=True)
        other_driver = Driver.objects.create(name="other", status=True)
        Rent.objects.create(driver=driver, summ=1000, payment_date=date(2023, 8, 15), time=time(9, 0, 0), balance=1000)

    def test_add_first_rent(self):
        responce = self.client.post("/api/accounting/rent/create/", self.first_rent_data, format="json")
        driver_rents = Rent.objects.filter(driver_id=2)
        self.assertEquals(responce.status_code, status.HTTP_201_CREATED)
        self.assertEquals(responce.data["balance"], 1000)
        self.assertEquals(len(driver_rents), 1)

    def test_add_next_rent(self):
        responce = self.client.post("/api/accounting/rent/create/", self.next_rent_data, format="json")
        driver_rents = Rent.objects.filter(driver_id=1)
        self.assertEquals(responce.status_code, status.HTTP_201_CREATED)
        self.assertEquals(responce.data["balance"], 2000)
        self.assertEquals(len(driver_rents), 2)
