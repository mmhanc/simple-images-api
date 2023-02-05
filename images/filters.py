from django_filters import rest_framework as filters

from images.models import Image


class ImageFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr="icontains")

    class Meta:
        model = Image
        fields = [
            "title",
        ]
