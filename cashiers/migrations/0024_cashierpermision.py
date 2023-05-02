# Generated by Django 4.0.7 on 2023-05-01 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cashiers', '0023_alter_cashierorders_customer_alter_kazang_customer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cashierpermision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('adminstatus', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'CASHIER PERMISION',
            },
        ),
    ]