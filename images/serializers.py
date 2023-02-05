import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            TemporaryUploadedFile)
from PIL import Image as PILImage
from rest_framework import serializers

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="image.url")

    class Meta:
        model = Image
        fields = ["id", "url", "title", "width", "height"]


class ImageCreateSerializer(serializers.ModelSerializer):
    keep_ratio = serializers.BooleanField(default=True, label="Keep aspect ratio")
    width = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    height = serializers.IntegerField(
        required=False,
        min_value=1,
    )

    class Meta:
        model = Image
        fields = ["id", "title", "width", "height", "image", "keep_ratio"]

    def validate(self, data):
        width = data.get("width")
        height = data.get("height")
        if not width and not height:
            raise serializers.ValidationError("Please specify width, height or both")

        image = data.get("image")
        keep_ratio = data.pop("keep_ratio")
        data["image"], data["width"], data["height"] = self.resize_in_memory_image(
            image, width, height, keep_ratio
        )

        return data

    @staticmethod
    def resize_in_memory_image(image, width, height, keep_ratio=True):
        current_image = BytesIO(image.read())
        pil_image = PILImage.open(current_image)

        if width and pil_image.width > width or height and pil_image.height > height:
            if not width:
                width = int(height * pil_image.width / pil_image.height)
            elif not height:
                height = int(width * pil_image.height / pil_image.width)

            size = (width, height)
            if keep_ratio:
                pil_image.thumbnail(size)
            else:
                pil_image = pil_image.resize(size)

        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = "JPEG" if img_format == "JPG" else img_format
        new_width, new_height = pil_image.width, pil_image.height
        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)
        new_image = ContentFile(new_image.getvalue())
        image = InMemoryUploadedFile(
            file=new_image,
            field_name=None,
            name=image.name,
            content_type=image.content_type,
            size=None,
            charset=None,
        )
        return image, new_width, new_height
