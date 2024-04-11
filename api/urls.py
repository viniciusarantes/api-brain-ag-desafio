from django.urls import include, path

urlpatterns = [
    path('', include('rural.urls'), name='rural'),
]
