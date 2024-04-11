from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rural.views import ProducerView

router = DefaultRouter()
router.register('producer', ProducerView, basename='producer')

urlpatterns = [
    path('', include(router.urls), name='producer')
]
