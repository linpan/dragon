# Generated by Django 3.1.3 on 2020-11-23 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('block5', '0025_auto_20201123_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npcnode',
            name='af',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='npc', to='block5.actioneffect'),
        ),
    ]
