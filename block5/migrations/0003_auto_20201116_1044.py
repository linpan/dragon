# Generated by Django 3.1.3 on 2020-11-16 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block5', '0002_auto_20201116_1010'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='description',
        ),
    ]