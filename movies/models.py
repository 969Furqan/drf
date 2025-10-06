from django.db import models

# Create your models here.
class Movies(models.Models):
    title = models.CharField(max_length=150)
    genres = models.JSONField(default=list)


    def __str__(self):
        return self.title

