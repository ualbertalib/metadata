# Generated by Django 2.1 on 2018-09-17 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Webapp', '0034_auto_20180914_1529'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='processing',
            unique_together={('name', 'uploaded_at', 'file_type', 'description', 'apis')},
        ),
    ]
