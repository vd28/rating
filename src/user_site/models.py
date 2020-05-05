from django.db import models
from core.models import Revision, University


class Config(models.Model):
    class Meta:
        verbose_name = 'configuration'
        verbose_name_plural = 'configurations'
        unique_together = ('university', 'revision')
        constraints = [
            models.UniqueConstraint(
                fields=['active'],
                condition=models.Q(active=True),
                name='one_active'
            )
        ]

    revision = models.ForeignKey(Revision, on_delete=models.PROTECT)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)



class Doc_knowledge(models.Model):
    class Meta:
        verbose_name = 'knowledge'
    TITLE_MAX_LENGTH = 2048

    field_of_knowledge = models.CharField(max_length=TITLE_MAX_LENGTH)
    number = models.IntegerField()
    university = models.ForeignKey(University, on_delete=models.CASCADE,default=0)

class Cooperating(models.Model):
    class Meta:
        verbose_name='cooperating'
    TITLE_MAX_LENGTH = 2048

    organization_name = models.CharField(max_length=TITLE_MAX_LENGTH)
    number=models.IntegerField()


