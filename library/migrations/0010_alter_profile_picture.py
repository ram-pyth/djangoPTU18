# Generated by Django 4.2.9 on 2024-01-15 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_bookreview_book_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='profile_pics/default.png', upload_to='profile_pics'),
        ),
    ]