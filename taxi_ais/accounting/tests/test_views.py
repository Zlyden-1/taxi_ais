from datetime import date
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
        for i in dates:
            Rent.objects.create(driver=driver, summ=summ, payment_date=i)

    def test_list_all(self):
        response = self.client.get(f"/api/accounting/rents/?start_date=2022-1-1&&end_date=2024-1-1")
        self.assertEquals(response.data, self.list_all_responce_data)

    # def test_list_for_last_week(self):
    #     response = self.client.get(f"/api/accounting/rents/")
    #     self.assertEquals(response.data, self.list_all_responce_data)
