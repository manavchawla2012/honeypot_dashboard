# Generated by Django 3.0.8 on 2020-08-03 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0003_auto_20200803_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalmanagergraphs',
            name='chart_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='graphs.GraphType'),
        ),
    ]
