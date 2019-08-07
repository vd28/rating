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
