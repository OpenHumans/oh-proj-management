# Generated by Django 2.0.7 on 2018-08-20 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0012_auto_20180615_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='S3Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]