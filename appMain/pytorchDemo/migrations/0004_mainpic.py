# Generated by Django 3.0.6 on 2020-05-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pytorchDemo', '0003_auto_20200512_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '首页图片管理',
                'verbose_name_plural': '首页图片管理',
            },
        ),
    ]