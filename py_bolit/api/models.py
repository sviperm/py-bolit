from django.db import models


class NodeType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='states')
    value = models.CharField(max_length=100)
    # TODO set max number
    distribution = models.FloatField(default=0.5)

    def __str__(self):
        return self.value


class Node(models.Model):
    # TODO only latin constraint
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey('NodeType', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.code


class Probability(models.Model):
    # TODO parent and child nodes mustn't be equals
    parent_state = models.ForeignKey('State', on_delete=models.CASCADE, related_name="parent")
    child_state = models.ForeignKey('State', on_delete=models.CASCADE, related_name="child")
    # TODO set max number
    value = models.FloatField()

    def __str__(self):
        return (f"{self.parent_state.node.name}: {self.parent_state.value} -> "
                f"{self.child_state.node.name}: {self.child_state.value} = "
                f"{self.value}")
