# Generated by Django 3.1.4 on 2020-12-28 00:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0011_auto_20201227_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='InforCollectReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('excute_date', models.CharField(max_length=50)),
                ('target_name', models.CharField(max_length=50)),
                ('target_url', models.CharField(max_length=1000)),
                ('target_location', models.CharField(max_length=50)),
                ('target_ip', models.CharField(max_length=50)),
                ('target_port', models.CharField(max_length=10)),
                ('target_warzone', models.CharField(max_length=10)),
                ('weakness', models.CharField(max_length=20)),
                ('search_time', models.CharField(max_length=20)),
                ('vpn_ip', models.CharField(max_length=20)),
                ('topic', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
                ('follow_up', models.CharField(max_length=1000)),
                ('status', models.IntegerField(default=0)),
                ('upload_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]