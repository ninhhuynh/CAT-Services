from django.db import models


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']


class TrainedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    desc = models.TextField()
    src_lang = models.CharField(max_length=50)
    tgt_lang = models.CharField(max_length=50)

    class Meta:
        ordering = ['created']


class SourceTranslation(models.Model):
    text = models.TextField()
    model_name = models.CharField(max_length=100)

    class Meta:
        unique_together = (('text', 'model_name'),)

    def __str__(self):
        return self.text


class TargetTranslation(models.Model):
    text = models.TextField()
    rank = models.IntegerField()
    src = models.ForeignKey(SourceTranslation, on_delete=models.CASCADE)
