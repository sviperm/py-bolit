# Generated by Django 2.2.12 on 2020-06-04 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200601_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='distribution',
        ),
        migrations.AddField(
            model_name='state',
            name='distribution',
            field=models.FloatField(default=0.5),
        ),
    ]
