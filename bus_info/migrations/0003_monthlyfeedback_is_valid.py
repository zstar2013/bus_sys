# Generated by Django 2.0.3 on 2018-04-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_info', '0002_monthlyfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyfeedback',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]