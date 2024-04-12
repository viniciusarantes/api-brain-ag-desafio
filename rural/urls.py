from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rural.views import PlantingViewSet, ProducerViewSet

router = DefaultRouter()
router.register('producer', ProducerViewSet, basename='producer')
router.register('planting', PlantingViewSet, basename='planting')

urlpatterns = [
    path('', include(router.urls), name='rural')
]
