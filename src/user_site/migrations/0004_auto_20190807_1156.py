# Generated by Django 2.2.4 on 2019-08-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0003_auto_20190803_1512'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='config',
            constraint=models.UniqueConstraint(condition=models.Q(active=True), fields=('active',), name='one_active'),
        ),
    ]
