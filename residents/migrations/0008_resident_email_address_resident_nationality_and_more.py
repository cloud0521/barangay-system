# Generated by Django 5.2.1 on 2025-05-20 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0007_alter_resident_civil_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='email_address',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='resident',
            name='nationality',
            field=models.CharField(blank=True, default='Filipino', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resident',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='resident',
            name='religion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='civil_status',
            field=models.CharField(choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('WIDOWED', 'Widowed'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated'), ('ANNULLED', 'Annulled'), ('COMMON-LAW / LIVE-IN PARTNER', 'Common-law / Live-in Partner')], max_length=50),
        ),
    ]
