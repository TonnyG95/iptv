# Generated by Django 4.2.4 on 2023-08-25 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0005_usersubscription_mag_mac_usersubscription_mag_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='mag_mac',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='mag_model',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='mag_sn',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]