# Generated by Django 4.2.4 on 2023-08-24 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0002_userprofile_mag_mac_adresa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mag_mac_adresa',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mag_model_uredjaja',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mag_sn',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
