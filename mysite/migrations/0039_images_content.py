# Generated by Django 3.1.5 on 2021-02-24 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0038_auto_20210220_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='content',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
