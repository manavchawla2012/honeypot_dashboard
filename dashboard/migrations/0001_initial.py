# Generated by Django 3.0.8 on 2020-07-16 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SnortDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sig_id', models.CharField(blank=True, max_length=60, null=True)),
                ('sig_rev', models.CharField(blank=True, max_length=30, null=True)),
                ('msg', models.CharField(blank=True, max_length=300, null=True)),
                ('proto', models.CharField(blank=True, max_length=30, null=True)),
                ('src', models.CharField(blank=True, max_length=117, null=True)),
                ('srcport', models.CharField(blank=True, max_length=30, null=True)),
                ('src_city', models.CharField(blank=True, max_length=135, null=True)),
                ('src_country', models.CharField(blank=True, max_length=135, null=True)),
                ('dst', models.CharField(blank=True, max_length=117, null=True)),
                ('dstport', models.CharField(blank=True, max_length=30, null=True)),
                ('dst_city', models.CharField(blank=True, max_length=135, null=True)),
                ('dst_country', models.CharField(blank=True, max_length=135, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('src_longitude', models.CharField(blank=True, max_length=45, null=True)),
                ('src_latitude', models.CharField(blank=True, max_length=45, null=True)),
                ('dst_longitude', models.CharField(blank=True, max_length=45, null=True)),
                ('dst_latitude', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'snort_details',
                'managed': True,
            },
        ),
    ]
