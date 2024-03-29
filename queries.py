from typing import Union
from django.db import models
from .models import Revision, PersonType, Person, ArticleItem, Department, Faculty


def fetch_latest_revision() -> Union[Revision, None]:
    return Revision.objects.order_by('-created_at').first()


def fetch_person_types() -> models.QuerySet:
    return PersonType.objects.prefetch_related('persons').order_by('name')


def search_persons(term: str) -> models.QuerySet:
    if not term:
        return Person.objects.none()

    search_lookups = (
        'full_name__icontains',
        'orcid__exact',
        'scopus_key__exact',
        'google_scholar_key__exact',
        'semantic_scholar_key__exact',
        'wos_key__exact'
    )

    cond = models.Q(**{search_lookups[0]: term})
    for lookup in search_lookups[1:]:
        cond |= models.Q(**{lookup: term})

    return Person.objects.filter(cond)


def fetch_faculties(university_id: int, annotate: bool = False) -> models.QuerySet:
    qs = Faculty.objects.filter(university_id=university_id)

    if annotate:
        qs = qs.annotate(
            orcid=models.Count('department__person__orcid'),
            scopus=models.Count('department__person__scopus_key'),
            google_scholar=models.Count('department__person__google_scholar_key'),
            semantic_scholar=models.Count('department__person__semantic_scholar_key'),
            wos=models.Count('department__person__wos_key')
        )

    return qs


def fetch_person(person_id: int, load_university: bool = False) -> Person:
    qs = Person.objects.all()
    if load_university:
        qs = qs.select_related('department__faculty__university')
    return qs.get(id=person_id)


def fetch_department(department_id: int) -> Department:
    qs = Department.objects.all()
    return qs.get(id=department_id)


def fetch_faculty(faculty_id: id) -> Faculty:
   qs = Faculty.objects.all()
   return qs.get(id=faculty_id)


def fetch_joints_authors(person_id: int) -> models.QuerySet:
    subquery = ArticleItem.objects.filter(person_id=person_id).values('article_id')
    return Person.objects \
        .filter(articleitem__article_id__in=models.Subquery(subquery)) \
        .annotate(articles_count=models.Count('id')) \
        .exclude(id=person_id) \
        .order_by('full_name')


def fetch_articles(person_id: int) -> models.QuerySet:
    return ArticleItem.objects.select_related('person', 'article').filter(person_id=person_id)
