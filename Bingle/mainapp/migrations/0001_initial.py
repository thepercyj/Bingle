# Generated by Django 4.2 on 2024-02-27 17:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(default='default', max_length=255, verbose_name='Book Title')),
                ('book_author', models.CharField(default='default', max_length=255, verbose_name='Book Author')),
                ('genre', models.CharField(default='default', max_length=255, verbose_name='Genre')),
                ('published_date', models.DateField(default=datetime.date(2024, 1, 1), verbose_name='Publish Date')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_location', models.CharField(default='default', max_length=255, verbose_name='Primary Location')),
                ('current_location', models.CharField(default='default', max_length=255, verbose_name='Current Location')),
                ('phone_number', models.CharField(default='default', max_length=255, verbose_name='Phone Number')),
                ('birth_date', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Birth Date')),
                ('review', models.IntegerField(null=True, verbose_name='Review Score')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.BooleanField(default=True, verbose_name='Available')),
                ('booked', models.CharField(default='default', max_length=255, verbose_name='Booked')),
                ('book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_books_book', to='mainapp.book')),
                ('currently_with', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currently_with', to='mainapp.userprofile')),
                ('owner_book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='mainapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(default='default', max_length=255, verbose_name='Details')),
                ('request_type', models.IntegerField(default=1, verbose_name='Request Type')),
                ('request_value', models.CharField(default='default', max_length=255, verbose_name='Request Value')),
                ('created_on', models.DateTimeField(default=datetime.datetime(2024, 1, 1, 12, 0), verbose_name='Created On')),
                ('modified_on', models.DateTimeField(default=datetime.datetime(2024, 1, 1, 12, 0), verbose_name='Modified On')),
                ('notification_status', models.IntegerField(default=1, verbose_name='Notification Status')),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='mainapp.userprofile')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='mainapp.userprofile')),
                ('user_book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages_user_book', to='mainapp.userbook')),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_user_1', to='mainapp.userprofile')),
                ('id_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_user_2', to='mainapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(default=datetime.date(2024, 1, 1), verbose_name='From Date')),
                ('to_date', models.DateField(default=datetime.date(2024, 1, 1), verbose_name='To Date')),
                ('returned', models.BooleanField(default=False, verbose_name='Returned')),
                ('borrower_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_borrower', to='mainapp.userprofile')),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_owner', to='mainapp.userprofile')),
            ],
        ),
    ]
