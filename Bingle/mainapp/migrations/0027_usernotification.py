# Generated by Django 4.2.11 on 2024-05-07 09:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0026_remove_notification_recipient'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, verbose_name='Created On')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='mainapp.notification')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='mainapp.userprofile')),
            ],
        ),
    ]
