# Generated by Django 3.1.5 on 2021-02-20 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0034_auto_20210219_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exploitreport',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='inforcollectreport',
            name='topic',
        ),
    ]
