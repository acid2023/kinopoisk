# Generated by Django 4.2.3 on 2024-03-11 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kinopoisk', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='tiltle',
            new_name='title',
        ),
    ]