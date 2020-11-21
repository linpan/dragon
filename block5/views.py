from django.shortcuts import render
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics
import django_filters.rest_framework
from .models import Scene, NPCNode, Goods, Actions, ActionEffect, NodeCheckout
from .serializers import SceneSerializer, NPCSerializer, NPCSerializerRetrieve, GoodSerializer, GoodsSerializerRetrieve, \
    ActionSerializer, AFSerializer, AFRetrieveSerializer, NodeSerializer, ActionEntrySerializer


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


class GoodList(FilterMixin, generics.ListCreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer


class GoodRetrieve(generics.RetrieveAPIView):
    lookup_field = 'node'
    serializer_class = GoodsSerializerRetrieve

    def get_queryset(self):
        scene = self.kwargs['scene']
        queryset = Goods.objects.filter(scene_id=scene)
        return queryset


class ActionList(FilterMixin, generics.ListCreateAPIView):
    queryset = Actions.objects.all()
    serializer_class = ActionSerializer


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
        npcs = NPCNode.objects.filter(scene=scene)
        actions = Actions.objects.filter(scene=scene)
        goods_serializer = GoodSerializer(goods, many=True)
        npcs_serializer = NPCSerializer(npcs, many=True)
        actions_serializer = ActionEntrySerializer(actions, many=True)
        entry['source'] = actions_serializer.data

        good_data = goods_serializer.data
        for good in good_data:
            good['target_type'] = 'good'

        npc_data = npcs_serializer.data
        for npc in npc_data:
            npc['target_type'] = 'npc'
        entry['target'] = npc_data + good_data

        return Response(entry)


