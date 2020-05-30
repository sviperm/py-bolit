from django.contrib import admin
from .models import NodeType, State, Node


@admin.register(NodeType)
class NodeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    pass
