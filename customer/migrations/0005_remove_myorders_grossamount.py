# Generated by Django 4.0.7 on 2023-01-24 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_myorders_incl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorders',
            name='grossamount',
        ),
    ]
