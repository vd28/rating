# Generated by Django 2.2.4 on 2019-08-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190812_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='source',
            field=models.CharField(blank=True, choices=[('imported', 'Imported')], max_length=30),
        ),
    ]
