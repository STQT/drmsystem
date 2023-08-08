# Generated by Django 4.1.9 on 2023-08-05 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0005_order_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]