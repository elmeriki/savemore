# Generated by Django 4.0.7 on 2023-02-02 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Swipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('swipsid', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'SWIPES',
            },
        ),
        migrations.CreateModel(
            name='Sts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recieptno', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'STS',
            },
        ),
        migrations.CreateModel(
            name='Qadadic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookno', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Qadadic',
            },
        ),
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnumber', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'OTHER PAPERS',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notenum', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'NOTES',
            },
        ),
    ]
