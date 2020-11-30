from django.shortcuts import render
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics
import django_filters.rest_framework
from .models import Scene, NPCNode, Goods, Actions, ActionEffect, NodeCheckout
from .serializers import SceneSerializer, NPCSerializer, NPCSerializerRetrieve, GoodSerializer, GoodsSerializerRetrieve, \
    ActionSerializer, AFSerializer, AFRetrieveSerializer, NodeSerializer, ActionEntrySerializer, GoodNodeSerializer, \
    NPCNodeSerializer


# Create your views here.
class FilterMixin:
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scene']


class SceneList(generics.ListCreateAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


class SceneRetrieve(generics.RetrieveAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


class NPCList(FilterMixin, generics.ListCreateAPIView):
    queryset = NPCNode.objects.all()
    serializer_class = NPCSerializer


class NPCRetrieve(generics.RetrieveAPIView):
    queryset = NPCNode.objects.all()
    lookup_field = 'node'
    serializer_class = NPCSerializerRetrieve

    def get_queryset(self):
        scene = self.kwargs['scene']
        queryset = NPCNode.objects.filter(scene_id=scene)
        return queryset


class GoodList(generics.ListCreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scene']


class GoodRetrieve(generics.RetrieveAPIView):
    lookup_field = 'node'
    serializer_class = GoodsSerializerRetrieve

    def get_queryset(self):
        scene = self.kwargs['scene']
        queryset = Goods.objects.filter(scene_id=scene)
        return queryset

class ActionList(generics.ListCreateAPIView):
    queryset = Actions.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scene']


class ActionRetrieve(generics.RetrieveAPIView):
    lookup_field = 'node'
    serializer_class = ActionSerializer

    def get_queryset(self):
        scene = self.kwargs['scene']
        queryset = Actions.objects.filter(scene_id=scene)
        return queryset


class AFList(FilterMixin, generics.ListCreateAPIView):
    queryset = ActionEffect.objects.all()
    serializer_class = AFSerializer


class AFRetrieve(generics.RetrieveAPIView):
    queryset = ActionEffect.objects.all()
    lookup_field = 'node'
    serializer_class = AFRetrieveSerializer

    def get_queryset(self):
        scene = self.kwargs['scene']
        queryset = ActionEffect.objects.filter(scene_id=scene)
        return queryset


class NodeCheckOutView(FilterMixin, generics.CreateAPIView):
    queryset = NodeCheckout.objects.all()
    serializer_class = NodeSerializer


class NodeCheckOutRetrive(generics.RetrieveAPIView):
    queryset = NodeCheckout.objects.all()
    lookup_field = 'scene'
    serializer_class = NodeSerializer


class Entry(APIView):
    def get(self, request):
        scene = self.request.GET.get('scene')
        entry = {}
        goods = Goods.objects.filter(scene=scene)
        npc = NPCNode.objects.filter(scene=scene)
        goods_serializer = NPCNodeSerializer(goods, many=True)
        npc_serializer = GoodNodeSerializer(npc, many=True)
        good_data = goods_serializer.data
        npc_data = npc_serializer.data
        entry['source'] = npc_data
        entry['target'] = npc_data + good_data

        return Response(entry)


class UpdateActionAndGood(APIView):
    """
    把动作放到物品里面
    """
    def post(self, request):
        scene = self.request.data.get('scene')
        action_id = self.request.data.get('action_id')
        good_id = self.request.data.get('good_id')
        act = Actions.objects.get(node=action_id, scene_id=scene)
        good = Goods.objects.get(node=good_id, scene_id=scene)
        act.goods = good
        act.save()
        return Response({'msg': act.id})


class UpdateGoodAndAction(APIView):
    """
    物品-> 动作
    """
    def post(self, request):
        scene = self.request.data.get('scene')
        action_id = self.request.data.get('action_id')
        good_id = self.request.data.get('good_id')
        act = Actions.objects.get(node=action_id, scene_id=scene)
        good = Goods.objects.get(node=good_id, scene_id=scene)
        good.action = act
        good.save()
        return Response({'msg': act.id})

