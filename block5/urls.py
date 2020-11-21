from django.urls import path, include
from .views import SceneList, SceneRetrieve, NPCList, NPCRetrieve, GoodList, GoodRetrieve, ActionList, ActionRetrieve, \
    AFList, Entry, AFRetrieve, NodeCheckOutView, NodeCheckOutRetrive

urlpatterns = [
    path('scene', SceneList.as_view()),
    path('npc', NPCList.as_view()),
    path('good', GoodList.as_view()),
    path('action', ActionList.as_view()),
    path('af', AFList.as_view()),
    path('scene/<int:pk>', SceneRetrieve.as_view()),
    path('af/<int:scene>/<int:node>/', AFRetrieve.as_view()),
    path('npc/<int:scene>/<int:node>/', NPCRetrieve.as_view()),
    path('good/<int:scene>/<int:node>/', GoodRetrieve.as_view()),
    path('action/<int:scene>/<int:node>/', ActionRetrieve.as_view()),
    path('entry', Entry.as_view()),
    path('node', NodeCheckOutView.as_view()),
    path('node/<int:scene>', NodeCheckOutRetrive.as_view()),
]