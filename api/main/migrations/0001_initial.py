# Generated by Django 4.1.9 on 2023-08-03 09:50

from django.db import migrations, models

def delete_objects(apps, schema_editor):
    User = apps.get_model('main', 'CustomUser')
    User.objects.get_or_create(id=1, username='noname', fullname='noname', user_lang='kz')


def reverse_pass(apps, schema_editor):
    # Object removal code
    ...


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, null=True)),
                ('fullname', models.CharField(max_length=255)),
                ('user_lang', models.CharField(default='kz', max_length=2)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_subscribed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(delete_objects, reverse_pass),
    ]
