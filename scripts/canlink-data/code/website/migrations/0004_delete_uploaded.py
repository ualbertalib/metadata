# Generated by Django 2.1 on 2018-11-13 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_uploaded_old_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Uploaded',
        ),
    ]
