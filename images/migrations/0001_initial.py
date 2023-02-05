# Generated by Django 4.1 on 2023-02-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('width', models.PositiveIntegerField(verbose_name='width')),
                ('height', models.PositiveIntegerField(verbose_name='height')),
                ('image', models.ImageField(upload_to='images')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
