# Generated by Django 4.0.1 on 2022-07-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_tle_submissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='submission_id',
        ),
        migrations.AddField(
            model_name='submission',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
