# Generated by Django 3.1.3 on 2020-11-17 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('block5', '0009_goods_goodsextraattrs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='NPC的名称')),
                ('node', models.CharField(max_length=32, verbose_name='节点编号')),
                ('type_node', models.CharField(max_length=32, verbose_name='节点类型')),
                ('transitive', models.FloatField(default=0)),
                ('attack_backswing', models.FloatField(default=0)),
                ('attack_duration', models.FloatField(default=0)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='block5.goods')),
                ('scene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='block5.scene')),
            ],
            options={
                'db_table': 'node_actions',
            },
        ),
    ]
