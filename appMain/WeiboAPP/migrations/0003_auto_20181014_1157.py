# Generated by Django 2.1.2 on 2018-10-14 03:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WeiboAPP', '0002_auto_20181013_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myself', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WeiboAPP.test')),
            ],
        ),
        migrations.AddField(
            model_name='mblog',
            name='comment',
            field=models.ManyToManyField(related_name='blog_comment_set', through='WeiboAPP.MblogComment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mblogcomment',
            name='refer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WeiboAPP.MblogComment'),
        ),
        migrations.AddField(
            model_name='mblogcomment',
            name='thumb',
            field=models.ManyToManyField(related_name='comment_thumb_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mblog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_author_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
