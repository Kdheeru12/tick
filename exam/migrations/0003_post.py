# Generated by Django 3.0.2 on 2020-08-26 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0002_challenge_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=800)),
                ('video', models.FileField(upload_to='')),
                ('upload_date', models.DateField(auto_now=True)),
                ('ip', models.GenericIPAddressField()),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('challenge', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exam.Challenge')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
