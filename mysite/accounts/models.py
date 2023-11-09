from django.db import models

class Task(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title