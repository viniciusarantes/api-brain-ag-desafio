from rest_framework import status, views, viewsets
from rest_framework.response import Response

from rural.models import Culture, Producer
from rural.serializers import (
    CULTURE_ADD_ACTION,
    CULTURE_REMOVE_ACTION,
    CultureSerializer,
    ProducerCulturesSerializer,
    ProducerSerializer,
    TotalFarmsSerializer,
)


class ProducerViewSet(viewsets.ModelViewSet):
    """
    Manage producer data
    """
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class CultureViewSet(viewsets.ModelViewSet):
    """
    Manage vegetable cultures data
    """
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer


class ProducerAddCultureView(views.APIView):
    """
    Add cultures for a producer
    """
    def post(self, request):
        data = request.POST.dict() or request.data
        serializer = ProducerCulturesSerializer(data=data, context={'action': CULTURE_ADD_ACTION})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProducerRemoveCultureView(views.APIView):
    """
    Remove cultures for a producer
    """
    def post(self, request):
        data = request.POST.dict() or request.data
        serializer = ProducerCulturesSerializer(data=data, context={'action': CULTURE_REMOVE_ACTION})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TotalFarmsView(views.APIView):
    """
    Return total of farms to dashboard
    """
    def get(self, request):
        producers = Producer.objects.all()
        serializer = TotalFarmsSerializer(producers)
        return Response(serializer.data, status=status.HTTP_200_OK)
