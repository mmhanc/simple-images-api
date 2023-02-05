from urllib.request import Request

import pytest
from django.test import RequestFactory
from rest_framework import status

from images.serializers import ImageCreateSerializer, ImageSerializer
from images.views import ImageViewSet


def api_setup_view(view, request, action=None, *args, **kwargs):
    view.request = request
    view.action = action
    view.args = args
    view.kwargs = kwargs
    return view


def new_image_payload(width, height, img, keep_ratio):
    return {
        "title": "test title",
        "width": width,
        "height": height,
        "image": img,
        "keep_ratio": keep_ratio,
    }


@pytest.mark.django_db
class TestImagesAPI:

    endpoint = "/api/images/"

    def test_list_status(self, client):
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK

    def test_put_method(self, client):
        response = client.put(self.endpoint)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_method(self, client):

        response = client.patch(self.endpoint)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_method(self, client):
        response = client.delete(self.endpoint)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize("action", ["list", "retrieve"])
    def test_get_serializer_class(self, action):
        factory = RequestFactory()
        viewset = ImageViewSet()
        request = factory.get(self.endpoint)
        api_setup_view(view=viewset, request=Request(request), action=action)
        assert viewset.serializer_class == ImageSerializer

    def test_get_serializer_class_create(self, jpg_image_100x100):
        factory = RequestFactory()
        viewset = ImageViewSet()
        with open(jpg_image_100x100.name, "rb") as img:
            payload = new_image_payload(50, 50, img, True)
            request = factory.post(self.endpoint, data=payload)
        api_setup_view(view=viewset, request=Request(request), action="create")
        assert viewset.get_serializer_class() == ImageCreateSerializer

    def create_image(self, client, payload):
        return client.post(self.endpoint, data=payload)

    @pytest.mark.parametrize(
        "width,height,keep_ratio,expected_width,expected_height",
        [
            (50, 50, True, 50, 50),
            (100, 50, True, 50, 50),
            (50, 50, False, 50, 50),
            (100, 50, False, 100, 50),
        ],
    )
    def test_can_create_and_get_image(
        self,
        client,
        jpg_image_100x100,
        width,
        height,
        keep_ratio,
        expected_width,
        expected_height,
    ):
        with open(jpg_image_100x100.name, "rb") as img:
            payload = new_image_payload(width, height, img, keep_ratio)
            response = self.create_image(client, payload)
        data = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert data.get("width") == expected_width
        assert data.get("height") == expected_height

        created_image_id = data.get("id")
        get_image_response = client.get(self.endpoint + f"{created_image_id}/")
        assert get_image_response.status_code == status.HTTP_200_OK

    def test_can_list_images(self, client, jpg_image_100x100):
        for i in range(3):
            with open(jpg_image_100x100.name, "rb") as img:
                payload = new_image_payload(50 + i, 50, img, True)
                self.create_image(client, payload)
        list_images_response = client.get(self.endpoint)
        assert list_images_response.status_code == status.HTTP_200_OK
        data = list_images_response.data
        assert data.get("count") == 3
