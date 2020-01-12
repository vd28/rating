# Generated by Django 2.2.4 on 2019-08-12 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190723_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='persons',
            field=models.ManyToManyField(blank=True, through='core.ArticleItem', to='core.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='articles',
            field=models.ManyToManyField(blank=True, through='core.ArticleItem', to='core.Article'),
        ),
    ]