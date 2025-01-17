# Generated by Django 2.2.6 on 2024-07-03 16:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='data_logging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=40)),
                ('Remote_Name', models.CharField(max_length=40)),
                ('Call_Time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('Cancel_Time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('name_of_site', models.CharField(max_length=40)),
                ('user_type', models.CharField(choices=[('Hospital', 'Hospital'), ('Hotel', 'Hotel'), ('Restaurant', 'Restaurant'), ('OPD', 'OPD'), ('Office', 'Office'), ('Other', 'Other')], max_length=40)),
                ('area_name', models.CharField(max_length=40)),
                ('latitude', models.CharField(max_length=40)),
                ('longitude', models.CharField(max_length=40)),
                ('time_to_respond_in_min', models.PositiveIntegerField()),
                ('colour_after_not_attending', models.CharField(max_length=40)),
                ('logo_image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('text_to_show_on_top', models.CharField(max_length=100)),
                ('grid_size_row', models.PositiveIntegerField()),
                ('grid_size_col', models.PositiveIntegerField()),
                ('frequency_of_report', models.CharField(choices=[('No', 'No'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Half yearly', 'Half yearly'), ('Yearly', 'Yearly')], max_length=40)),
                ('Email_ID_for_report_1', models.CharField(blank=True, max_length=150)),
                ('gateway_device_code', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Remote_information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway_device_code', models.CharField(max_length=40)),
                ('remote_code', models.CharField(max_length=40)),
                ('remote_name', models.CharField(blank=True, max_length=40, null=True)),
                ('remote_type', models.CharField(choices=[('call', 'call'), ('cancel', 'cancel')], default='call', max_length=40)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='remote_information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
