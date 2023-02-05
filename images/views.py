from rest_framework import permissions, viewsets

from images.filters import ImageFilter
from images.models import Image
from images.serializers import ImageCreateSerializer, ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    create_serializer_class = ImageCreateSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = ImageFilter
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        if self.action == "create" and hasattr(
            self,
            "create_serializer_class",
        ):
            return self.create_serializer_class
        return super().get_serializer_class()
