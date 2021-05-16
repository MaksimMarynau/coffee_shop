# Generated by Django 3.1.7 on 2021-05-08 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_board', '0009_auto_20210508_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
        migrations.AddField(
            model_name='product',
            name='country',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Draft'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(upload_to='products/additional/', verbose_name='Image'),
        ),
        migrations.DeleteModel(
            name='ProductDescription',
        ),
    ]