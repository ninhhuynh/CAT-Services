from rest_framework.fields import IntegerField
import similarity
from django.db import models

# Create your models here.


class TranslationMemory(models.Model):
    name = models.TextField()
    src_lang = models.TextField()
    tgt_lang = models.TextField()


class SegmentPair(models.Model):
    src = models.ForeignKey(TranslationMemory, on_delete=models.CASCADE)
    src_segment = models.TextField()
    tgt_segment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Similarity(models.Model):
    src = models.TextField()
    tgt = models.TextField()
    similarity = models.IntegerField()


class SourceSimilarity(models.Model):
    text = models.TextField()


class TargetSimilarity(models.Model):
    text = models.TextField()
    similarity = models.IntegerField()
    src = models.ForeignKey(SourceSimilarity, on_delete=models.CASCADE)


# Functions for database
