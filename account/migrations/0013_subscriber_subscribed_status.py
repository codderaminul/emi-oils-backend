# Generated by Django 4.2.6 on 2023-12-26 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='subscribed_status',
            field=models.BooleanField(default=False),
        ),
    ]
