# Generated by Django 5.0.6 on 2024-07-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0004_jobinterview"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobinterview",
            name="reschedule_by",
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name="jobinterview",
            name="reschedule_end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="jobinterview",
            name="reschedule_start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
