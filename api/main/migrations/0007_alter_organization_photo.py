# Generated by Django 4.1.9 on 2023-08-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_organization_photo_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
