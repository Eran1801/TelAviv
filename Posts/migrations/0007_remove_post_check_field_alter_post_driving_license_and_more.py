# Generated by Django 4.2.4 on 2023-09-12 07:14

import Posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0006_post_check_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='check_field',
        ),
        migrations.AlterField(
            model_name='post',
            name='driving_license',
            field=models.FileField(upload_to=Posts.models.generate_unique_filename),
        ),
        migrations.AlterField(
            model_name='post',
            name='proof_image',
            field=models.FileField(upload_to=Posts.models.generate_unique_filename),
        ),
    ]
