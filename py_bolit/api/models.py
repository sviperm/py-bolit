from django.db import models


class NodeType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='states')
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.value}"


class Node(models.Model):
    # TODO only latin constraint
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey('NodeType', on_delete=models.SET_NULL, null=True)
    # TODO set max number
    distribution = models.FloatField()

    def __str__(self):
        return f"{self.code} {self.distribution}"


class Probability(models.Model):
    # TODO parent and child nodes mustn't be equals
    parent_state = models.ForeignKey('State', on_delete=models.CASCADE, related_name="parent")
    child_state = models.ForeignKey('State', on_delete=models.CASCADE, related_name="child")
    # TODO set max number
    value = models.FloatField()
