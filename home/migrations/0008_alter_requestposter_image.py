# Generated by Django 3.2 on 2022-07-12 18:30

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_requestposter_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestposter',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]