# Generated by Django 5.0.1 on 2024-01-16 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
