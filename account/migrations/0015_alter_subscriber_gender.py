# Generated by Django 4.2.6 on 2024-01-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_company_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Unspecified', 'Unspecified'), ('OTHER', 'OTHER')], default='Unspecified', max_length=20),
        ),
    ]
