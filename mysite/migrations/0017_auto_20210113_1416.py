# Generated by Django 3.1.5 on 2021-01-13 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0016_auto_20210112_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='exploitreport',
            name='image',
            field=models.ImageField(default=' ', upload_to='image/'),
        ),
        migrations.AlterField(
            model_name='exploitreport',
            name='content',
            field=models.JSONField(max_length=1000),
        ),
    ]
