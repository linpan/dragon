from rest_framework import serializers
from django.forms.models import model_to_dict

from .models import Scene, Team, Location, Role, Job, Gender, ItemType, NPCNode, NPCExtraAttrs, Goods, GoodsExtraAttrs, \
    Actions, ActionExtraAttrs, ActionEffect, NodeCheckout


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name']


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'name']


class SceneSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    location = LocationSerializer(many=True)
    role = RoleSerializer(many=True)
    job = JobSerializer(many=True)
    gender = GenderSerializer(many=True)
    item = ItemTypeSerializer(many=True)

    class Meta:
        model = Scene
        fields = ('id', 'name', 'team', 'location', 'role', 'gender', 'job', 'item', 'updated_at')

    def create(self, validated_data):
        team = validated_data.pop('team')
        location = validated_data.pop('location')
        role = validated_data.pop('role')
        gender = validated_data.pop('gender')
        item = validated_data.pop('item')
        job = validated_data.pop('job')

        scene = Scene.objects.create(**validated_data)
        # team options
        team_obj = [Team(scene=scene, **t) for t in team if t['name']]
        Team.objects.bulk_create(team_obj)
        # location options
        location_obj = [Location(scene=scene, **t) for t in location if t['name']]
        Location.objects.bulk_create(location_obj)
        # role options
        role_obj = [Role(scene=scene, **t) for t in role if t['name']]
        Role.objects.bulk_create(role_obj)

        # gender option
        gender_obj = [Gender(scene=scene, **t) for t in gender if t['name']]
        Gender.objects.bulk_create(gender_obj)

        # item type option
        item_obj = [ItemType(scene=scene, **t) for t in item if t['name']]
        ItemType.objects.bulk_create(item_obj)
        # job option
        job_obj = [Job(scene=scene, **t) for t in job if t['name']]
        Job.objects.bulk_create(job_obj)

        return scene


class NPCAttrsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPCExtraAttrs
        fields = ['id', 'name', 'value', 'type']



class NPCSerializer(serializers.ModelSerializer):
    attrs = NPCAttrsSerializer(many=True)

    class Meta:
        model = NPCNode
        fields = ('id', 'name', 'scene', 'node', 'type_node', 'role',
                  'team', 'job', 'gender', 'attrs')

    def create(self, validated_data):
        """
        https://www.cnblogs.com/iiiiiher/p/11646309.html
        """
        attrs = validated_data.pop('attrs')
        node = validated_data.pop('node')
        type_node = validated_data.pop("type_node")
        scene = validated_data.pop('scene')
        npc, created = NPCNode.objects.update_or_create(scene=scene, node=node, type_node=type_node, defaults=validated_data)
        # try:
        #     npc = NPCNode.objects.get(node=node, type_node=type_node)
        #     for key, value in validated_data.items():
        #         setattr(npc, key, value)
        #     npc.save()
        # except NPCNode.DoesNotExist:
        #     new_values = {'node': node, 'type_node': type_node}
        #     new_values.update(validated_data)
        #     npc = NPCNode(**new_values)
        #     npc.save()

        if attrs:
            npc.attrs.all().delete()
            NPCExtraAttrs.objects.bulk_create([
                NPCExtraAttrs(npc=npc, **extra)
                for extra in attrs
            ])
        return npc


class NPCSerializerRetrieve(serializers.ModelSerializer):
    attrs = NPCAttrsSerializer(many=True)
    team = TeamSerializer()
    role = RoleSerializer()
    job = JobSerializer()
    gender = JobSerializer()

    class Meta:
        model = NPCNode
        fields = ('id', 'name', 'scene', 'node', 'type_node', 'role',
                  'team', 'job', 'gender', 'attrs')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


class GoodsSerializerRetrieve(serializers.ModelSerializer):
    attrs = NPCAttrsSerializer(many=True)
    item_type = serializers.SerializerMethodField('get_item')
    actions = serializers.SerializerMethodField('get_action')

    class Meta:
        model = Goods
        fields = ('id', 'name', 'scene', 'node', 'type_node', 'attrs', 'item_type', 'actions')

    def get_item(self, obj):
        return model_to_dict(obj.item_type)

    def get_action(self, obj):
        print(obj.actions.all())
        return obj.actions.values()


class GoodRelatedActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        exclude = ('item_type', 'action', 'scene')


class GoodSerializer(serializers.ModelSerializer):
    attrs = NPCAttrsSerializer(many=True)
    actions = GoodRelatedActionSerializer(many=True)

    class Meta:
        model = Goods
        fields = ('id', 'name', 'node', 'type_node', 'item_type', 'attrs', 'actions', 'scene')

    def create(self, validated_data):
        attrs = validated_data.pop('attrs')
        actions = validated_data.pop('actions')  # 关联动作
        node = validated_data.pop('node')
        type_node = validated_data.pop("type_node")
        scene = validated_data.get('scene')
        good, created = Goods.objects.update_or_create(node=node, type_node=type_node, defaults=validated_data)
        if attrs:
            good.attrs.all().delete()
            GoodsExtraAttrs.objects.bulk_create([
                GoodsExtraAttrs(goods=good, **extra)
                for extra in attrs
            ])
        if actions:
            good.actions.all().delete()
            Actions.objects.bulk_create([
              Actions(goods=good, scene=scene, **extra)
              for extra in actions
            ])

        return good


class GoodActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'name',  'type_node', 'node', 'item_type')


class ActionEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Actions
        fields = ('id', 'name', 'node', 'type_node',  'scene',
                  'attack_duration', 'attack_backswing', 'transitive', 'is_transitive_verb')



class ActionSerializer(serializers.ModelSerializer):
    attrs = NPCAttrsSerializer(many=True)
    good = GoodActionSerializer(many=True)
    # 必须是关联的外箭

    class Meta:
        model = Actions
        fields = ('id', 'name', 'node', 'type_node', 'attrs', 'scene',
                  'attack_duration', 'attack_backswing', 'transitive', 'is_transitive_verb',
                  'good')

    def create(self, validated_data):
        attrs = validated_data.pop('attrs')
        good = validated_data.pop('good')
        scene = validated_data.get('scene')
        node = validated_data.pop('node')
        type_node = validated_data.pop("type_node")
        act, created = Actions.objects.update_or_create(node=node, type_node=type_node, defaults=validated_data)
        if attrs:
            act.attrs.all().delete()
            ActionExtraAttrs.objects.bulk_create([
                ActionExtraAttrs(action=act, **extra)
                for extra in attrs
            ])
       # todo if 不搭配动作呢
        act.good.all().delete()
        Goods.objects.bulk_create([
            Goods(action=act, scene=scene,  **extra)
            for extra in good
        ])
        return act


class AFSerializer(serializers.ModelSerializer):
    target = serializers.CharField(write_only=True)
    target_type = serializers.CharField(write_only=True)

    class Meta:
        model = ActionEffect
        fields = ('id', 'scene', 'action', 'name', 'node', 'type_node',
                  'condition', 'effect', 'target', 'target_type')

    def create(self, validated_data):
        target = validated_data.pop("target")
        target_type = validated_data.pop("target_type")
        node = validated_data.pop('node')
        type_node = validated_data.pop("type_node")
        af, created = ActionEffect.objects.update_or_create(node=node, type_node=type_node, defaults=validated_data)
        if target_type == 'npc':
            af.good_id = None
            af.npc_id = target
        else:
            af.npc_id = None
            af.good_id = target
        af.save()
        return af


class AFRetrieveSerializer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField('get_source')
    target = serializers.SerializerMethodField('get_target')

    class Meta:
        model = ActionEffect
        fields = ('id', 'scene', 'action', 'name', 'node', 'type_node',
                  'condition', 'effect', 'target')

    def get_source(self, obj):
        return model_to_dict(obj.action)

    def get_target(self, obj):
        if obj.npc_id:
            data = model_to_dict(obj.npc)
            data['target_type'] = 'npc'
            return data
        else:
            data = model_to_dict(obj.good)
            data['target_type'] = 'good'
            return data


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeCheckout
        fields = '__all__'

    def create(self, validated_data):
        scene = validated_data.pop('scene')
        node, created = NodeCheckout.objects.update_or_create(scene=scene, defaults=validated_data)
        return node
