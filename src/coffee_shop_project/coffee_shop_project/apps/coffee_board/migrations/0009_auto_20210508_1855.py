# Generated by Django 3.1.7 on 2021-05-08 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_board', '0008_auto_20210502_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/additional/', verbose_name='Image'),
        ),
    ]
