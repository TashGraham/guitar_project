# Generated by Django 2.2.28 on 2024-07-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guitar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='pic',
            field=models.ImageField(blank=True, upload_to='part_images'),
        ),
    ]
