# Generated by Django 4.2.4 on 2023-08-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0004_rename_mag_mac_adresa_userprofile_mag_mac_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='mag_mac',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='mag_model',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='mag_sn',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
