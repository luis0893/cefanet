# Generated by Django 2.1.1 on 2018-09-12 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recog', '0020_userfeeditem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfeeditem',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='UserFeedItem',
        ),
    ]
