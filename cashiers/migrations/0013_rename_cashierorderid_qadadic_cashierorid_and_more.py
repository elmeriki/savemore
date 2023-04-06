# Generated by Django 4.0.7 on 2023-04-01 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashiers', '0012_remove_kazang_bookno_remove_notes_bookno_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qadadic',
            old_name='cashierorderid',
            new_name='cashierorid',
        ),
        migrations.AlterField(
            model_name='cashierorders',
            name='comment',
            field=models.TextField(blank=True, default='NA', null=True),
        ),
        migrations.AlterField(
            model_name='cashierorders',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cashierorders',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
