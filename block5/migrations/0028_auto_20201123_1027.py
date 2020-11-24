# Generated by Django 3.1.3 on 2020-11-23 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('block5', '0027_auto_20201123_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='npcnode',
            name='af',
        ),
        migrations.AlterField(
            model_name='npcnode',
            name='af_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='npc_source', to='block5.actioneffect'),
        ),
        migrations.AlterField(
            model_name='npcnode',
            name='af_target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='npc_target', to='block5.actioneffect'),
        ),
    ]
