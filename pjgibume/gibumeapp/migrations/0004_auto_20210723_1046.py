# Generated by Django 3.2 on 2021-07-23 01:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gibumeapp', '0003_auto_20210723_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfume',
            name='dislike_users',
            field=models.ManyToManyField(blank=True, default='', related_name='dislike_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='perfume',
            name='hate_users',
            field=models.ManyToManyField(blank=True, default='', related_name='hate_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='perfume',
            name='like_users',
            field=models.ManyToManyField(blank=True, default='', related_name='like_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='perfume',
            name='love_users',
            field=models.ManyToManyField(blank=True, default='', related_name='love_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='perfume',
            name='ok_users',
            field=models.ManyToManyField(blank=True, default='', related_name='ok_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]