# Generated by Django 4.1.9 on 2023-08-18 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_organization_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['order']},
        ),
    ]
