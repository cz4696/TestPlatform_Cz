# Generated by Django 2.2.7 on 2021-04-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestPlatform_User', '0002_auto_20210418_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_data',
            name='pj_pn',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
