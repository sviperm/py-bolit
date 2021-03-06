from django.contrib import admin
from .models import NodeType, State, Node, Probability


@admin.register(NodeType)
class NodeTypeAdmin(admin.ModelAdmin):
    pass


class StateInline(admin.TabularInline):
    model = State
    extra = 0


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    inlines = [
        StateInline,
    ]


@admin.register(Probability)
class ProbabilityAdmin(admin.ModelAdmin):
    pass
