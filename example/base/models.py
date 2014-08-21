from django.db import models


class ParentModel(models.Model):
    text = models.TextField()


class SampleModel(models.Model):
    parent = models.ForeignKey(ParentModel)
    text = models.TextField()
    number = models.IntegerField()
    char = models.CharField(max_length=5)
