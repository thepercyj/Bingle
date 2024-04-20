# Generated by Django 4.2.11 on 2024-04-20 18:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0020_remove_booking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(default=datetime.date(2024, 1, 1), verbose_name='From Date')),
                ('to_date', models.DateField(default=datetime.date(2024, 1, 1), verbose_name='To Date')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending', max_length=10)),
                ('conversation_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_conversation', to='mainapp.conversation')),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_owner', to='mainapp.userprofile')),
                ('user_book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_user_book', to='mainapp.userbook')),
            ],
        ),
    ]
