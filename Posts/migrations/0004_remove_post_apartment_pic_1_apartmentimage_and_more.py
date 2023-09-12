# Generated by Django 4.2.4 on 2023-09-11 08:55

import Posts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0003_alter_post_post_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='apartment_pic_1',
        ),
        migrations.CreateModel(
            name='ApartmentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=Posts.models.generate_unique_filename)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartment_images_related', to='Posts.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='apartment_images',
            field=models.ManyToManyField(related_name='posts', to='Posts.apartmentimage'),
        ),
    ]