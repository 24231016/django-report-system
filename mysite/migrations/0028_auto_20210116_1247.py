# Generated by Django 3.1.5 on 2021-01-16 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0027_auto_20210113_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exploitreport',
            name='image',
            field=models.ImageField(upload_to='img/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='inforcollectreport',
            name='content',
            field=models.JSONField(),
        ),
    ]