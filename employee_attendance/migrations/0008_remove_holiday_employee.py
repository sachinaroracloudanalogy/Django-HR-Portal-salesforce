# Generated by Django 2.0.5 on 2018-07-17 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_attendance', '0007_holiday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holiday',
            name='employee',
        ),
    ]
