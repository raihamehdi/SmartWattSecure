# Generated by Django 5.0 on 2024-11-26 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartwatt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anomaly',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='anomaly',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
