# Generated by Django 3.0.2 on 2020-08-26 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='slug',
            new_name='slug1',
        ),
    ]