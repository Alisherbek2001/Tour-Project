# Generated by Django 5.0.6 on 2024-07-01 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='comment',
            field=models.TextField(),
        ),
    ]
