# Generated by Django 4.0.7 on 2023-03-24 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashiers', '0002_rename_notenum_notes_bookno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='qadadic',
            name='cashierorderid',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashiers.cashierorders'),
        ),
    ]