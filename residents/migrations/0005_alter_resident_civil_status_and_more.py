# Generated by Django 5.2.1 on 2025-05-20 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0004_alter_resident_contact_information_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='civil_status',
            field=models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Separated', 'Separated'), ('Annulled', 'Annulled'), ('Common-law / Live-in Partner', 'Common-law / Live-in Partner')], max_length=50),
        ),
        migrations.AlterField(
            model_name='resident',
            name='contact_information',
            field=models.CharField(blank=True, default='+63', max_length=100, null=True),
        ),
    ]
