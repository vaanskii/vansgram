# Generated by Django 5.0.1 on 2024-01-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_friends_count_alter_friendshiprequests_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='posts_count',
            field=models.IntegerField(default=0),
        ),
    ]
