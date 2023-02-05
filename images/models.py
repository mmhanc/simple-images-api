from django.db import models


class Image(models.Model):
    title = models.CharField(verbose_name="title", max_length=255)
    width = models.PositiveIntegerField(verbose_name="width")
    height = models.PositiveIntegerField(verbose_name="height")
    image = models.ImageField(upload_to="images")

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"
