# Generated by Django 5.0.6 on 2024-07-01 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_booking_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'verbose_name': 'Booking', 'verbose_name_plural': 'Bookings'},
        ),
    ]
