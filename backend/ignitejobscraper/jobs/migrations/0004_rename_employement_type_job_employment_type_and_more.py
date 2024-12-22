# Generated by Django 5.1.4 on 2024-12-22 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_remove_job_skills_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='employement_type',
            new_name='employment_type',
        ),
        migrations.AlterField(
            model_name='job',
            name='job_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location_type',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
