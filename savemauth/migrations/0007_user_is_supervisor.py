# Generated by Django 4.0.7 on 2023-03-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savemauth', '0006_rename_subburb_user_subb'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_supervisor',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]