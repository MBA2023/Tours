# Generated by Django 4.2.5 on 2023-10-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0009_alter_tourimage_tour'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='max_participants',
            field=models.PositiveIntegerField(default=15, verbose_name='Максимальное количество человек на экскурсии'),
        ),
    ]