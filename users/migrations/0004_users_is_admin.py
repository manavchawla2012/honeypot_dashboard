# Generated by Django 3.0.8 on 2020-07-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200720_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
