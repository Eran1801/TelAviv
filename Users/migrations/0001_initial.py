# Generated by Django 4.2.4 on 2023-08-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_full_name', models.CharField(max_length=30)),
                ('user_password', models.CharField(max_length=20)),
                ('user_email', models.CharField(max_length=50)),
                ('user_phone', models.CharField(max_length=20)),
            ],
        ),
    ]