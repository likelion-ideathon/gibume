# Generated by Django 3.2 on 2021-08-04 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gibumeapp', '0008_alter_communitycomment_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='communitycomment',
            old_name='post',
            new_name='title',
        ),
    ]