# Generated by Django 3.0.6 on 2020-05-14 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0005_compatt'),
    ]

    operations = [
        migrations.AddField(
            model_name='comppic',
            name='title',
            field=models.CharField(default='测试作品', max_length=100),
            preserve_default=False,
        ),
    ]
