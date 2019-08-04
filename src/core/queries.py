from typing import Union, Tuple

from django.db.models import QuerySet

from . import models


def fetch_latest_revision() -> Union[models.Revision, None]:
    return models.Revision.objects.order_by('-created_at').first()


def fetch_person_types() -> QuerySet:
    return models.PersonType.objects.prefetch_related('persons').order_by('name')
