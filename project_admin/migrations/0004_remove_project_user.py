# Generated by Django 2.0.2 on 2018-02-20 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0003_auto_20180220_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
    ]
