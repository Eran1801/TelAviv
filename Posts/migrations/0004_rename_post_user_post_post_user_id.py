# Generated by Django 4.2.4 on 2023-08-15 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0003_remove_post_apartment_pic_2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_user',
            new_name='post_user_id',
        ),
    ]