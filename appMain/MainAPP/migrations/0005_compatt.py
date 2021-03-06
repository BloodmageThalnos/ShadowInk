# Generated by Django 3.0.6 on 2020-05-14 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainAPP', '0004_auto_20200514_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompAtt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compatt_comp_set', to='MainAPP.Competition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compatt_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '参赛人员管理',
                'verbose_name_plural': '参赛人员管理',
            },
        ),
    ]
