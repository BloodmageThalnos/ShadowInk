# Generated by Django 2.1.1 on 2018-10-05 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LoginAPP', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]