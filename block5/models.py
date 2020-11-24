from django.db import models
from django.contrib.postgres.fields import ArrayField


class Scene(models.Model):
    name = models.CharField(max_length=64, verbose_name="场景")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "scene"
        ordering = ('-updated_at',)


class Team(models.Model):
    name = models.CharField(max_length=64, verbose_name="阵营")
    scene = models.ForeignKey(Scene, related_name='team', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'team'


class Location(models.Model):
    name = models.CharField(max_length=64, verbose_name="位置", blank=True, null=True)
    scene = models.ForeignKey(Scene, related_name='location',  on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'location'


class Role(models.Model):
    name = models.CharField(max_length=64, verbose_name="角色")
    scene = models.ForeignKey(Scene, related_name='role', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'


class Job(models.Model):
    name = models.CharField(max_length=64, verbose_name="职业")
    scene = models.ForeignKey(Scene, related_name='job', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'job'


class Gender(models.Model):
    name = models.CharField(max_length=64, verbose_name="性别")
    scene = models.ForeignKey(Scene, related_name='gender', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gender'


class ItemType(models.Model):
    name = models.CharField(max_length=64, verbose_name="人物类型")
    scene = models.ForeignKey(Scene, related_name='item', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item_type'


class NPCNode(models.Model):
    scene = models.ForeignKey(Scene, related_name='npc', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name="NPC的名称")
    node = models.CharField(max_length=32, verbose_name='节点编号')
    type_node = models.CharField(max_length=32, verbose_name='节点类型')

    # the common attribute from scene
    team = models.ForeignKey(Team, related_name='npc',  on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, related_name='npc',  on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ForeignKey(Job, related_name='npc',  on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.ForeignKey(Gender, related_name='npc',  on_delete=models.SET_NULL, null=True, blank=True)
    target = models.ForeignKey('ActionEffect', related_name='npc_target',
                               on_delete=models.SET_NULL, null=True, blank=True, verbose_name='来自af的我目标')
    source = models.ForeignKey('ActionEffect', related_name='npc_source',
                               on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='来自af的动作源')

    def __str__(self):
        return self.node

    class Meta:
        db_table = 'node_npc'


class NPCExtraAttrs(models.Model):
    npc = models.ForeignKey(NPCNode, related_name='attrs', on_delete=models.CASCADE)
    name = models.CharField(max_length=16, verbose_name='属性名')
    value = models.CharField(max_length=16, verbose_name='属性值')
    type = models.CharField(max_length=8, verbose_name='数据类型')

    def __str__(self):
        return self.npc

    class Meta:
        db_table = 'node_npc_extra_attrs'


class Goods(models.Model):
    scene = models.ForeignKey(Scene, related_name='goods', on_delete=models.CASCADE)
    action = models.ForeignKey('Actions', related_name='good', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=64, verbose_name="NPC的名称")
    node = models.CharField(max_length=32, verbose_name='节点编号')
    type_node = models.CharField(max_length=32, verbose_name='节点类型')

    item_type = models.ForeignKey(ItemType, related_name='good', on_delete=models.CASCADE)
    af = models.ForeignKey('ActionEffect', related_name='good', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'node_goods'


class GoodsExtraAttrs(models.Model):
    goods = models.ForeignKey(Goods, related_name='attrs', on_delete=models.CASCADE)
    name = models.CharField(max_length=16, verbose_name='属性名')
    value = models.CharField(max_length=16, verbose_name='属性值')
    type = models.CharField(max_length=8, verbose_name='数据类型')

    def __str__(self):
        return self.goods

    class Meta:
        db_table = 'node_goods_extra_attrs'


class Actions(models.Model):
    scene = models.ForeignKey(Scene, related_name='actions', on_delete=models.CASCADE)

    goods = models.ForeignKey(Goods, related_name='actions', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=64, verbose_name="NPC的名称")
    node = models.CharField(max_length=32, verbose_name='节点编号')
    type_node = models.CharField(max_length=32, verbose_name='节点类型')
    is_transitive_verb = models.BooleanField(default=False)
    transitive = models.FloatField(default=0)
    attack_backswing = models.FloatField(default=0)
    attack_duration = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'node_actions'


class ActionExtraAttrs(models.Model):
    action = models.ForeignKey(Actions, related_name='attrs', on_delete=models.CASCADE)
    name = models.CharField(max_length=16, verbose_name='属性名')
    value = models.CharField(max_length=16, verbose_name='属性值')
    type = models.CharField(max_length=8, verbose_name='数据类型')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'node_action_extra_attrs'


class ActionEffect(models.Model):
    """
    fix: af 1:n  npc/goodgi
    """

    scene = models.ForeignKey(Scene, related_name='af', on_delete=models.CASCADE)

    name = models.CharField(max_length=64, verbose_name="af的名称")
    node = models.CharField(max_length=32, verbose_name='节点编号')
    type_node = models.CharField(max_length=32, verbose_name='节点类型')
    condition = models.TextField(blank=True, null=True)
    effect = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'node_af'


class NodeCheckout(models.Model):
    scene = models.ForeignKey(Scene, related_name='node', on_delete=models.CASCADE)
    node = models.TextField(verbose_name='节点图信息')
    info = models.TextField(verbose_name='节点名称映射表')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.updated_at)

    class Meta:
        db_table = 'node_checkout'




