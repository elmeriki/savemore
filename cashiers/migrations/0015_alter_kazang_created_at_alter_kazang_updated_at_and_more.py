# Generated by Django 4.0.7 on 2023-04-04 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashiers', '0014_alter_qadadic_options_alter_kazang_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kazang',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='kazang',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='swipes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='swipes',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
