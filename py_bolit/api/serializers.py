from .models import NodeType, Node
from rest_framework import serializers


class NodeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeType
        fields = ['id', 'name']


class NodeSerializer(serializers.ModelSerializer):
    node_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = Node
        fields = ['code', 'name', 'description', 'node_type', 'distribution']