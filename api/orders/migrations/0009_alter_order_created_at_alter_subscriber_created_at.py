# Generated by Django 4.1.9 on 2023-08-29 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_created_at_alter_subscriber_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]