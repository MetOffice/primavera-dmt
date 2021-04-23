# Generated by Django 3.2 on 2021-04-23 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('version', models.CharField(blank=True, max_length=200, verbose_name='Version')),
            ],
            options={
                'verbose_name': 'Dataset',
                'unique_together': {('name', 'version')},
            },
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='File name')),
                ('incoming_directory', models.CharField(max_length=4096, verbose_name='Incoming directory')),
                ('directory', models.CharField(blank=True, max_length=4096, verbose_name='Directory')),
                ('size', models.BigIntegerField(verbose_name='File size')),
                ('checksum_value', models.CharField(max_length=200)),
                ('checksum_type', models.CharField(choices=[('SHA256', 'SHA256'), ('MD5', 'MD5'), ('ADLER32', 'ADLER32')], max_length=20)),
                ('online', models.BooleanField(default=True, verbose_name='Online?')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dmt_app.dataset', verbose_name='Dataset')),
            ],
            options={
                'verbose_name': 'Data File',
                'unique_together': {('name', 'incoming_directory')},
            },
        ),
    ]
