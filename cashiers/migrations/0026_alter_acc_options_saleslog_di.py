# Generated by Django 4.0.7 on 2023-05-18 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashiers', '0025_acc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acc',
            options={'verbose_name_plural': 'ACC'},
        ),
        migrations.AddField(
            model_name='saleslog',
            name='di',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True),
        ),
    ]
