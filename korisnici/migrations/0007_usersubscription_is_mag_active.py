# Generated by Django 4.2.4 on 2023-08-25 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0006_alter_usersubscription_mag_mac_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='is_mag_active',
            field=models.BooleanField(default=False),
        ),
    ]
