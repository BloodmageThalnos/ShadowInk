# Generated by Django 3.0.6 on 2020-05-14 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0003_comppic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
