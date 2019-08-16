from typing import Tuple, Optional, Iterable, Dict, List

from django.db import models

from .models import Person, Faculty, Department, SnapshotOptions
from .paginator import Paginator


class AbstractRatingBuilder(Paginator):
    snapshot_lookup = '{snapshot}__{field}'

    def __init__(self, snapshot_options: SnapshotOptions):
        super().__init__()
        self.options = snapshot_options
        self.revision_id = None
        self.set_ordering(self.options.ordering)
        self.field_lookups = self.get_field_lookups()

    def build(self):
        if self.revision_id is None:
            raise ValueError('revision must be set')
        return super().build()

    def set_ordering(self, ordering: Optional[Tuple[str, ...]] = None) -> 'AbstractRatingBuilder':
        super().set_ordering(ordering)
        if len(self.ordering) == 0:
            self.ordering = self.options.ordering
        return self

    def set_revision(self, revision_id: int) -> 'AbstractRatingBuilder':
        self.revision_id = revision_id
        return self

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        options = {
            self.field_lookups[field]: models.F(self.get_snapshot_lookup(field))
            for field in self.options.fields
        }
        return qs.annotate(**options)

    def get_snapshot_lookup(self, field: str) -> str:
        return self.snapshot_lookup.format(snapshot=self.options.name, field=field)

    def get_field_lookups(self) -> Dict[str, str]:
        return {field: f'{self.options.name}_{field}' for field in self.options.fields}


class DepartmentRatingBuilder(AbstractRatingBuilder):
    snapshot_lookup = 'person__{snapshot}__{field}'
    search_lookups = ('name__icontains',)

    def __init__(self, snapshot_options: SnapshotOptions):
        super().__init__(snapshot_options)
        self.university_id = None
        self.faculty_id = None

    def get_field_lookups(self):
        field_lookups = super().get_field_lookups()
        field_lookups.update({'name': 'name'})
        return field_lookups

    def set_university(self, university_id: int) -> 'DepartmentRatingBuilder':
        self.university_id = university_id
        self.faculty_id = None
        return self

    def set_faculty(self, faculty_id: int) -> 'DepartmentRatingBuilder':
        self.university_id = None
        self.faculty_id = faculty_id
        return self

    def get_queryset(self) -> models.QuerySet:
        qs = Department.objects \
            .filter(**{self.get_snapshot_lookup('revision_id'): self.revision_id})

        if self.university_id is not None:
            qs = qs.filter(faculty__university_id=self.university_id)

        elif self.faculty_id is not None:
            qs = qs.filter(faculty_id=self.faculty_id)

        return qs.distinct()

    def build(self):
        if [self.university_id, self.faculty_id].count(None) == 2:
            raise ValueError('university or faculty must be set')
        return super().build()

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        window = {'partition_by': [models.F('id')]}
        options = {
            self.field_lookups[field]: models.Window(
                **window,
                expression=models.Max(self.get_snapshot_lookup(field))
            )
            for field in self.options.fields
        }
        return qs.annotate(**options)

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering + ['id']


class FacultyRatingBuilder(AbstractRatingBuilder):
    snapshot_lookup = 'department__person__{snapshot}__{field}'
    search_lookups = ('name__icontains',)

    def __init__(self, snapshot_options: SnapshotOptions):
        super().__init__(snapshot_options)
        self.university_id = None

    def get_field_lookups(self):
        field_lookups = super().get_field_lookups()
        field_lookups.update({'name': 'name'})
        return field_lookups

    def set_university(self, university_id: int) -> 'FacultyRatingBuilder':
        self.university_id = university_id
        return self

    def get_queryset(self) -> models.QuerySet:
        return Faculty.objects \
            .filter(university_id=self.university_id) \
            .filter(**{self.get_snapshot_lookup('revision_id'): self.revision_id}) \
            .distinct()

    def build(self):
        if self.university_id is None:
            raise ValueError('university must be set')
        return super().build()

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        window = {'partition_by': [models.F('id')]}
        options = {
            self.field_lookups[field]: models.Window(
                **window,
                expression=models.Max(self.get_snapshot_lookup(field))
            )
            for field in self.options.fields
        }
        return qs.annotate(**options)

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering + ['id']


class PersonRatingBuilder(AbstractRatingBuilder):
    search_lookups = (
        'full_name__icontains', 'orcid__exact', 'scopus_key__exact',
        'google_scholar_key__exact', 'semantic_scholar_key__exact',
        'wos_key__exact'
    )
    prefetch_related = ('person_types',)

    def __init__(self, snapshot_options: SnapshotOptions):
        super().__init__(snapshot_options)
        self.university_id = None
        self.faculty_id = None
        self.department_id = None
        self.person_type_ids = []

    def get_field_lookups(self):
        field_lookups = super().get_field_lookups()
        field_lookups.update({'full_name': 'full_name'})
        return field_lookups

    def set_university(self, university_id: int) -> 'PersonRatingBuilder':
        self.university_id = university_id
        self.faculty_id = None
        self.department_id = None
        return self

    def set_faculty(self, faculty_id: int) -> 'PersonRatingBuilder':
        self.university_id = None
        self.faculty_id = faculty_id
        self.department_id = None
        return self

    def set_department(self, department_id: int) -> 'PersonRatingBuilder':
        self.university_id = None
        self.faculty_id = None
        self.department_id = department_id
        return self

    def set_person_types(self, person_type_ids: Iterable[int]) -> 'PersonRatingBuilder':
        self.person_type_ids = tuple(person_type_ids)
        return self

    def get_queryset(self) -> models.QuerySet:
        qs = Person.objects \
            .filter(**{self.get_snapshot_lookup('revision_id'): self.revision_id})

        if self.university_id is not None:
            qs = qs.filter(department__faculty__university_id=self.university_id)

        elif self.faculty_id is not None:
            qs = qs.filter(department__faculty_id=self.faculty_id)

        elif self.department_id is not None:
            qs = qs.filter(department_id=self.department_id)

        if len(self.person_type_ids) > 0:
            qs = qs.filter(person_types__id__in=tuple(self.person_type_ids))

        return qs.distinct()

    def build(self):
        if [self.university_id, self.faculty_id, self.department_id].count(None) == 3:
            raise ValueError('university, faculty or department must be set')
        return super().build()

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering + ['id']
