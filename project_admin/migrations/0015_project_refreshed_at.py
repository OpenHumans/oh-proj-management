# Generated by Django 2.0.7 on 2018-08-23 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0014_auto_20180821_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='refreshed_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]