from typing import Union

from django.db.models import QuerySet, Q

from . import models


def fetch_latest_revision() -> Union[models.Revision, None]:
    return models.Revision.objects.order_by('-created_at').first()


def fetch_person_types() -> QuerySet:
    return models.PersonType.objects.prefetch_related('persons').order_by('name')


def search_persons(term: str) -> QuerySet:
    if not term:
        return models.Person.objects.none()

    search_lookups = (
        'full_name__icontains',
        'orcid__exact',
        'scopus_key__exact',
        'google_scholar_key__exact',
        'semantic_scholar_key__exact',
        'wos_key__exact'
    )

    cond = Q(**{search_lookups[0]: term})
    for lookup in search_lookups[1:]:
        cond |= Q(**{lookup: term})

    return models.Person.objects.filter(cond)
