# Generated by Django 3.0.8 on 2020-08-04 17:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttackPatternType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('description', models.CharField(max_length=5000)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'attack_pattern_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CourseOfAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('generic_id', models.CharField(blank=True, max_length=20, null=True)),
                ('action', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'course_of_action',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='IdentityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('description', models.CharField(max_length=5000)),
                ('label', models.CharField(blank=True, max_length=45, null=True)),
                ('identity_class', models.CharField(max_length=45)),
                ('sectors', models.CharField(blank=True, max_length=45, null=True)),
                ('contact_information', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'identity_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MalwareLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('description', models.CharField(max_length=5000)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'malware_label',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StixType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('identifier', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'stix_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StixFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('stix_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stix.StixType')),
            ],
            options={
                'db_table': 'stix_files',
                'managed': True,
            },
        ),
    ]
