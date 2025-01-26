from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    role = models.TextField(blank=True)
    available_time = models.JSONField(default = dict)

    def __str__(self):
        return self.id
