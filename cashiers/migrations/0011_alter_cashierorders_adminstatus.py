# Generated by Django 4.0.7 on 2023-03-26 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashiers', '0010_cashierorders_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashierorders',
            name='adminstatus',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
