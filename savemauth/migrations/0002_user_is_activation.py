# Generated by Django 4.0.7 on 2023-01-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savemauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_activation',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
