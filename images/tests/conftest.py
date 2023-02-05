import tempfile

import pytest
from PIL import Image as PILImage
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def jpg_image_100x100():
    image = PILImage.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    return tmp_file


@pytest.fixture
def png_image_200x200():
    image = PILImage.new('RGB', (200, 200))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(tmp_file)
    return tmp_file
