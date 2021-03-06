# Generated by Django 3.1.5 on 2021-02-20 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0037_auto_20210220_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='ex_post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.exploitreport'),
        ),
        migrations.AlterField(
            model_name='images',
            name='ic_post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.inforcollectreport'),
        ),
        migrations.AlterField(
            model_name='images',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.user'),
        ),
    ]
