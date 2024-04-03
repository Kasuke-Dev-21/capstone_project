# Generated by Django 5.0.2 on 2024-03-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_alter_report_map'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='type',
            field=models.CharField(choices=[('Accident', 'Accident'), ('Damaged Area', 'Damaged Area'), ('Design Flaw', 'Design Flaw'), ('Electrical Appliance', 'Electrical Appliance'), ('Flammable', 'Flammable'), ('Explosive', 'Explosive'), ('Substance', 'Substance'), ('Unknown', 'Unknown')], max_length=255, null=True),
        ),
    ]
