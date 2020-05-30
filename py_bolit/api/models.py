from django.db import models


class NodeType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    node = models.ForeignKey('NodeType', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.node.code} {self.value}"


class Node(models.Model):
    # добавить ограничение на латинские буквы в код
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    node_type = models.ForeignKey('NodeType', on_delete=models.SET_NULL, null=True)
    distribution = models.FloatField()

    def __str__(self):
        return f"{self.code} {self.distribution}"


class Probability(models.Model):
    # родитель и ребенок должны быть разными узлами
    parent_state = models.ForeignKey('State', on_delete=models.CASCADE, related_name="parent")
    child_state = models.ForeignKey('State', on_delete=models.CASCADE, related_name="child")
    value = models.FloatField()
