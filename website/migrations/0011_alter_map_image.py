# Generated by Django 5.0.2 on 2024-03-10 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_map_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='image',
            field=models.ImageField(null=True, upload_to='building_maps/'),
        ),
    ]
