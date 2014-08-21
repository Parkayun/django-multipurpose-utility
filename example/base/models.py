from django.db import models


class SampleModel(models.Model):
    text = models.TextField()
    number = models.IntegerField()
    char = models.CharField(max_length=5)
