from rest_framework import viewsets

from rural.models import Producer
from rural.serializers import ProducerSerializer


class ProducerView(viewsets.ModelViewSet):
    """
    Manage producer data
    """
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
