# Generated by Django 2.1.1 on 2018-09-12 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recog', '0017_auto_20180911_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
