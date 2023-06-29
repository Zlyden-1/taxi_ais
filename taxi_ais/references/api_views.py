from rest_framework.generics import ListAPIView

from .models import Driver
from .serializers import DriverSerializer


class DriversListAPI(ListAPIView):
    queryset = Driver.objects.all()
    serializer = DriverSerializer
