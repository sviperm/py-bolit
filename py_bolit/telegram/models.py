from django.db import models
from django.db.utils import IntegrityError


class Chat(models.Model):
    id = models.IntegerField(primary_key=True)


class Node(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100, default='')

    class Meta:
        unique_together = ('chat', 'code',)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            return True
        except IntegrityError:
            return False
