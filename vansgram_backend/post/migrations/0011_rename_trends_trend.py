# Generated by Django 5.0.1 on 2024-01-18 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_rename_trend_trends'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trends',
            new_name='Trend',
        ),
    ]
