# Generated by Django 3.2 on 2021-08-04 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gibumeapp', '0007_rename_title_communitycomment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitycomment',
            name='post',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='gibumeapp.community'),
        ),
    ]
