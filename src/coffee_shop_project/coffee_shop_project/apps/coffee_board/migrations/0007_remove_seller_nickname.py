# Generated by Django 3.1.7 on 2021-05-01 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_board', '0006_auto_20210429_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='nickname',
        ),
    ]