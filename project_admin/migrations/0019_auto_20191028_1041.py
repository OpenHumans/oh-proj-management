# Generated by Django 2.0.7 on 2019-10-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0018_remove_project_request_message_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='registered_datatypes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='requested_sources',
            field=models.TextField(default=''),
        ),
    ]