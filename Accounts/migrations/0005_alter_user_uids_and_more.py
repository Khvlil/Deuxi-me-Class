# Generated by Django 4.1.3 on 2022-12-11 01:32

import datetime
from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_alter_user_uids_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uids',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default='AtuWmnnTkMqwvntFrhe6Tw', editable=False, max_length=22, verbose_name='UIDS'),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='free_trial_expired',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 1, 32, 16, 175551, tzinfo=datetime.timezone.utc), verbose_name='Free trial expiration'),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='subscription_expired',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 1, 32, 16, 175551, tzinfo=datetime.timezone.utc), verbose_name='Subscription expiration'),
        ),
    ]
