# Generated by Django 3.1.3 on 2020-11-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block5', '0003_auto_20201116_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='位置'),
        ),
    ]