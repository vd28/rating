# Generated by Django 2.2.3 on 2019-07-13 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190713_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='person_types',
            field=models.ManyToManyField(to='core.PersonType'),
        ),
    ]
