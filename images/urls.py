from django.urls import include, path
from rest_framework import routers

from images.views import ImageViewSet

router = routers.DefaultRouter()

router.register('images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
