# Generated by Django 2.0.5 on 2018-07-31 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_attendance', '0017_reimbursement_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reimbursement',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
