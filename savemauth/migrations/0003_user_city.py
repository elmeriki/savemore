# Generated by Django 4.0.7 on 2023-01-20 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savemauth', '0002_user_is_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]
