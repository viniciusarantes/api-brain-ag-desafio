from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rural.views import (
    CultureViewSet,
    ProducerAddCultureView,
    ProducerRemoveCultureView,
    ProducerViewSet,
)

router = DefaultRouter()
router.register('producer', ProducerViewSet, basename='producer')
router.register('culture', CultureViewSet, basename='culture')

urlpatterns = [
    path('', include(router.urls), name='rural'),
    path('producer/add_culture', ProducerAddCultureView.as_view(), name='addculture'),
    path('producer/remove_culture', ProducerRemoveCultureView.as_view(), name='removeculture')
]
