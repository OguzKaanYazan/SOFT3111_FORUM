# Generated by Django 3.0 on 2020-01-03 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_auto_20200103_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='shuttlehours',
            name='hour',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='shuttlehours',
            name='quota',
            field=models.IntegerField(null=True),
        ),
    ]
