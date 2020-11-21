# Generated by Django 3.1.3 on 2020-11-16 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block5', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gender',
            name='name',
            field=models.CharField(default=1, max_length=64, verbose_name='性别'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemtype',
            name='name',
            field=models.CharField(default=1, max_length=64, verbose_name='人物类型'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='name',
            field=models.CharField(default=1, max_length=64, verbose_name='职业'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(default=1, max_length=64, verbose_name='位置'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='role',
            name='name',
            field=models.CharField(default=1, max_length=64, verbose_name='角色'),
            preserve_default=False,
        ),
    ]
