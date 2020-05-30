from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'get_types', views.NodeTypeListViewSet)
router.register(r'get_nodes', views.NodeListViewSet)
router.register(r'get_node', views.NodeViewSet, basename='get_node')
router.register(r'predict', views.PredictViewSet, basename='predict')

urlpatterns = [
    path('', include(router.urls)),
]
