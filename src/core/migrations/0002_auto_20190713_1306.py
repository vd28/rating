# Generated by Django 2.2.3 on 2019-07-13 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name': 'faculty', 'verbose_name_plural': 'faculties'},
        ),
        migrations.AlterModelOptions(
            name='university',
            options={'verbose_name': 'university', 'verbose_name_plural': 'universities'},
        ),
    ]
