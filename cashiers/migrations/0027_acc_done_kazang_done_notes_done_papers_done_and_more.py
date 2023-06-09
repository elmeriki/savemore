# Generated by Django 4.0.7 on 2023-05-29 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashiers', '0026_alter_acc_options_saleslog_di'),
    ]

    operations = [
        migrations.AddField(
            model_name='acc',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='kazang',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='notes',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='papers',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='qadadic',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sts',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='swipes',
            name='done',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
