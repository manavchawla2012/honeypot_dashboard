# Generated by Django 3.0.8 on 2020-07-20 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_login_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='login_expiry',
            field=models.DateTimeField(null=True),
        ),
    ]
