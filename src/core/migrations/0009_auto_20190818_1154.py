# Generated by Django 2.2.4 on 2019-08-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190817_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='revision',
            options={'permissions': (('can_import_revision', 'Can import revision'),)},
        ),
        migrations.AlterField(
            model_name='revision',
            name='source',
            field=models.CharField(blank=True, choices=[('import', 'Import')], max_length=30),
        ),
    ]