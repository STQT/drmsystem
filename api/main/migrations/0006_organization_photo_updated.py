# Generated by Django 4.1.9 on 2023-08-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_organization_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='photo_updated',
            field=models.BooleanField(default=False),
        ),
    ]
