# Generated by Django 2.1 on 2018-09-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webapp', '0029_progress_archive_process_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='processing',
            name='apis',
            field=models.CharField(blank=True, max_length=355),
        ),
        migrations.AlterField(
            model_name='processing',
            name='description',
            field=models.CharField(blank=True, max_length=355),
        ),
        migrations.AlterField(
            model_name='processing',
            name='name',
            field=models.CharField(blank=True, max_length=355),
        ),
    ]
