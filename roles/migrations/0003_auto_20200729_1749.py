# Generated by Django 3.0.8 on 2020-07-29 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0002_auto_20200729_1747'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='rolepermissions',
            constraint=models.UniqueConstraint(fields=('role', 'permission'), name='unique_role_permission'),
        ),
    ]
