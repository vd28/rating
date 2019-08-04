import textwrap

from django.db import models
from django.utils import formats

from .rating_builder import Options


class University(models.Model):
    class Meta:
        verbose_name = 'university'
        verbose_name_plural = 'universities'

    NAME_MAX_LENGTH = 1024

    name = models.CharField(max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    class Meta:
        verbose_name = 'faculty'
        verbose_name_plural = 'faculties'

    NAME_MAX_LENGTH = 1024

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Department(models.Model):
    NAME_MAX_LENGTH = 1024

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PersonType(models.Model):
    NAME_MAX_LENGTH = 1024

    name = models.CharField(max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class Person(models.Model):
    FULL_NAME_MAX_LENGTH = 1024

    full_name = models.CharField(max_length=FULL_NAME_MAX_LENGTH)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    articles = models.ManyToManyField('Article', through='ArticleItem')
    person_types = models.ManyToManyField(PersonType, related_name='persons', blank=True)

    orcid = models.CharField(
        verbose_name='ORCID', max_length=19, unique=True, blank=True, null=True
    )

    scopus_key = models.CharField(
        verbose_name='Scopus Key', max_length=50, unique=True, blank=True, null=True
    )

    google_scholar_key = models.CharField(
        verbose_name='Google Scholar Key', max_length=50, unique=True, blank=True, null=True
    )

    semantic_scholar_key = models.CharField(
        verbose_name='Semantic Scholar Key', max_length=50, unique=True, blank=True, null=True
    )

    wos_key = models.CharField(
        verbose_name='Web of Science Key', max_length=50, unique=True, blank=True, null=True
    )

    def __str__(self):
        return self.full_name


class Revision(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return formats.date_format(self.created_at, 'SHORT_DATETIME_FORMAT')


class AbstractSnapshot(models.Model):
    class Meta:
        abstract = True
        unique_together = ('revision', 'person')

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)

    @staticmethod
    def get_options():
        raise NotImplementedError


class ScopusSnapshot(AbstractSnapshot):
    class Meta(AbstractSnapshot.Meta):
        verbose_name = 'Scopus Snapshot'
        verbose_name_plural = 'Scopus Snapshots'

    h_index = models.PositiveIntegerField(verbose_name=' h-index', default=0)
    documents = models.PositiveIntegerField(default=0)
    citations = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_options():
        return Options(
            name='scopussnapshot',
            fields={'h_index', 'documents', 'citations'},
            ordering=('-h_index', '-documents', '-citations'),
        )


class GoogleScholarSnapshot(AbstractSnapshot):
    class Meta(AbstractSnapshot.Meta):
        verbose_name = 'Google Scholar Snapshot'
        verbose_name_plural = 'Google Scholar Snapshots'

    h_index = models.PositiveIntegerField(verbose_name=' h-index', default=0)
    citations = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_options():
        return Options(
            name='googlescholarsnapshot',
            fields={'h_index', 'citations'},
            ordering=('-h_index', '-citations'),
        )


class SemanticScholarSnapshot(AbstractSnapshot):
    class Meta(AbstractSnapshot.Meta):
        verbose_name = 'Semantic Scholar Snapshot'
        verbose_name_plural = 'Semantic Scholar Snapshots'

    citation_velocity = models.PositiveIntegerField(default=0)
    influential_citation_count = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_options():
        return Options(
            name='semanticscholarsnapshot',
            fields={'citation_velocity', 'influential_citation_count'},
            ordering=('-citation_velocity', '-influential_citation_count'),
        )


class WosSnapshot(AbstractSnapshot):
    class Meta(AbstractSnapshot.Meta):
        verbose_name = 'Web of Science Snapshot'
        verbose_name_plural = 'Web of Science Snapshots'

    publications = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_options():
        return Options(
            name='wossnapshot',
            fields={'publications'},
            ordering=('-publications',),
        )


class Article(models.Model):
    TITLE_MAX_LENGTH = 2048

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    persons = models.ManyToManyField(Person, through='ArticleItem')

    def __str__(self):
        return textwrap.shorten(self.title, width=50, placeholder='...')


class ArticleItem(models.Model):
    class Meta:
        unique_together = ('article', 'person')

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    scopus = models.BooleanField(default=False, verbose_name='Scopus')
    google_scholar = models.BooleanField(default=False, verbose_name='Google Scholar')
    semantic_scholar = models.BooleanField(default=False, verbose_name='Semantic Scholar')
    wos = models.BooleanField(default=False, verbose_name='Web of Science')
