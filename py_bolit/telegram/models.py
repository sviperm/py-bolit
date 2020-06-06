from django.db import models
from django.db.utils import IntegrityError


class Chat(models.Model):
    NONE = ''
    RESULT = 'r'
    START = 's'
    STATUS_CHOICES = [
        (NONE, ''),
        (RESULT, 'result'),
        (START, 'start'),
    ]
    id = models.IntegerField(primary_key=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=NONE,
    )

    def set_start_status(self):
        if self.status != self.START:
            self.status = self.START
            self.save()
        return self

    def set_result_status(self):
        if self.status != self.RESULT:
            self.status = self.RESULT
            self.save()
        return self

    @property
    def is_result_status(self):
        return self.status == self.RESULT


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
