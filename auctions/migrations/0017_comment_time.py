# Generated by Django 4.1.5 on 2023-02-15 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_remove_listing_winner_alter_listing_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
