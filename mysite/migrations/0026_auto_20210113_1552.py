# Generated by Django 3.1.5 on 2021-01-13 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0025_auto_20210113_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exploitreport',
            name='content',
        ),
        migrations.AddField(
            model_name='exploitreport',
            name='con',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]
