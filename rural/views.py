from rest_framework import viewsets

from rural.models import Planting, Producer
from rural.serializers import PlantingSerializer, ProducerSerializer


class ProducerViewSet(viewsets.ModelViewSet):
    """
    Manage producer data
    """
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class PlantingViewSet(viewsets.ModelViewSet):
    """
    Manage planting data
    """
    queryset = Planting.objects.all()
    serializer_class = PlantingSerializer
