from typing import Tuple, Optional, Any, Iterable, Dict, List

from django.db import models

from . import models as core_models


class RatingBuilderError(Exception):
    pass


class PageDoesNotExist(RatingBuilderError):
    def __init__(self, page: int):
        super().__init__(f'The page {page} doest not exist.')
        self.page = page


class FieldDoesNotExist(RatingBuilderError):
    def __init__(self, field: str):
        super().__init__(f'The field {repr(field)} does not exist.')
        self.field = field


class Options:
    __slots__ = ('name', 'fields', 'ordering')

    def __init__(self, name: str, fields: Iterable[str], ordering: Iterable[str]):
        self.name = name
        self.fields = set(fields)
        self.ordering = tuple(ordering)


class Pagination:
    __slots__ = ('page', 'limit')

    def __init__(self, page: int, limit: int):
        if page < 1:
            raise ValueError("'page' must be greater than 0")

        if limit < 1:
            raise ValueError("'per_page' must be greater than 0")

        self.page = page
        self.limit = limit

    @property
    def range(self) -> Tuple[int, int]:
        offset = (self.page - 1) * self.limit
        return offset, offset + self.limit


class Results:
    __slots__ = ('objects', 'total', 'page', 'limit')

    def __init__(self, objects: Iterable[Any], total: int, page: int = 1, limit: int = 1):
        self.objects = tuple(objects)
        self.total = total
        self.page = page
        self.limit = limit


class AbstractRatingBuilder:
    path_to_snapshot = '{snapshot}__{field}'
    search_lookups = ()

    def __init__(self, snapshot_options: Options):
        self.options = snapshot_options
        self.term = None
        self.pagination = None
        self.revision_id = None
        self.ordering = self.options.ordering
        self.field_lookups = self.build_field_lookups()

    def build(self):
        if self.revision_id is None:
            raise ValueError('revision must be set')

        qs = self.get_queryset().filter(**{self.build_snapshot_field_lookup('revision_id'): self.revision_id})

        qs = self.sort(qs)
        qs = self.annotate(qs)
        qs = self.search(qs)
        total = qs.count()
        qs = self.paginate(qs)

        objects = tuple(qs)
        pagination = self.pagination or Pagination(page=1, limit=total or 1)

        if len(objects) == 0 and pagination.page != 1:
            raise PageDoesNotExist(page=pagination.page)

        return Results(
            objects=tuple(qs),
            total=total,
            page=pagination.page,
            limit=pagination.limit
        )

    def get_queryset(self) -> models.QuerySet:
        raise NotImplementedError

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        options = {
            self.field_lookups[field]: models.F(self.build_snapshot_field_lookup(field))
            for field in self.options.fields
        }
        return qs.annotate(**options)

    def sort(self, qs: models.QuerySet) -> models.QuerySet:
        ordering = []
        for field in self.ordering:
            desc = field.startswith('-')
            if desc:
                field = field[1:]
            if field not in self.field_lookups:
                raise FieldDoesNotExist(field)
            ordering.append(f'-{self.field_lookups[field]}' if desc else self.field_lookups[field])

        ordering = self.make_ordering_deterministic(ordering)
        return qs.order_by(*ordering)

    def paginate(self, qs: models.QuerySet) -> models.QuerySet:
        if self.pagination is None:
            return qs

        left, right = self.pagination.range
        return qs[left:right]

    def search(self, qs: models.QuerySet) -> models.QuerySet:
        if len(self.search_lookups) == 0 or self.term is None:
            return qs

        cond = models.Q(**{**{self.search_lookups[0]: self.term}})
        for lookup in self.search_lookups[1:]:
            cond |= models.Q(**{lookup: self.term})

        return qs.filter(cond)

    def set_revision(self, revision_id: int) -> 'AbstractRatingBuilder':
        self.revision_id = revision_id
        return self

    def set_pagination(self, pagination: Optional[Pagination] = None) -> 'AbstractRatingBuilder':
        self.pagination = pagination
        return self

    def set_ordering(self, ordering: Optional[Tuple[str, ...]] = None) -> 'AbstractRatingBuilder':
        self.ordering = ordering or self.options.ordering
        return self

    def set_term(self, term: Optional[str] = None) -> 'AbstractRatingBuilder':
        self.term = term
        return self

    def build_snapshot_field_lookup(self, field: str) -> str:
        return self.path_to_snapshot.format(snapshot=self.options.name, field=field)

    def build_field_lookups(self) -> Dict[str, str]:
        return {field: f'{self.options.name}_{field}' for field in self.options.fields}

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering


class DepartmentRatingBuilder(AbstractRatingBuilder):
    path_to_snapshot = 'person__{snapshot}__{field}'
    search_lookups = ('name__icontains',)

    def __init__(self, snapshot_options: Options):
        super().__init__(snapshot_options)
        self.faculty_id = None

    def build_field_lookups(self):
        fields_map = super().build_field_lookups()
        fields_map.update({'name': 'name'})
        return fields_map

    def set_faculty(self, faculty_id: int) -> 'DepartmentRatingBuilder':
        self.faculty_id = faculty_id
        return self

    def get_queryset(self) -> models.QuerySet:
        return core_models.Department.objects.filter(faculty_id=self.faculty_id).distinct()

    def build(self):
        if self.faculty_id is None:
            raise ValueError('faculty must be set')
        return super().build()

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        window = {'partition_by': [models.F('id')]}
        options = {
            self.field_lookups[field]: models.Window(
                **window,
                expression=models.Max(self.build_snapshot_field_lookup(field))
            )
            for field in self.options.fields
        }
        return qs.annotate(**options)

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering + ['id']


class FacultyRatingBuilder(AbstractRatingBuilder):
    path_to_snapshot = 'department__person__{snapshot}__{field}'
    search_lookups = ('name__icontains',)

    def __init__(self, snapshot_options: Options):
        super().__init__(snapshot_options)
        self.university_id = None

    def build_field_lookups(self):
        fields_map = super().build_field_lookups()
        fields_map.update({'name': 'name'})
        return fields_map

    def set_university(self, university_id: int) -> 'FacultyRatingBuilder':
        self.university_id = university_id
        return self

    def get_queryset(self) -> models.QuerySet:
        return core_models.Faculty.objects.filter(university_id=self.university_id).distinct()

    def build(self):
        if self.university_id is None:
            raise ValueError('university must be set')
        return super().build()

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        window = {'partition_by': [models.F('id')]}
        options = {
            self.field_lookups[field]: models.Window(
                **window,
                expression=models.Max(self.build_snapshot_field_lookup(field))
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

    def __init__(self, snapshot_options: Options):
        super().__init__(snapshot_options)
        self.university_id = None
        self.person_type_ids = []

    def build_field_lookups(self):
        fields_map = super().build_field_lookups()
        fields_map.update({'full_name': 'full_name'})
        return fields_map

    def set_university(self, university_id: int) -> 'PersonRatingBuilder':
        self.university_id = university_id
        return self

    def set_person_types(self, person_type_ids: Iterable[int]) -> 'PersonRatingBuilder':
        self.person_type_ids = person_type_ids
        return self

    def get_queryset(self) -> models.QuerySet:
        qs = core_models.Person.objects.filter(department__faculty__university_id=self.university_id)
        if len(self.person_type_ids) > 0:
            qs = qs.filter(person_types__id__in=tuple(self.person_type_ids))
        return qs

    def build(self):
        if self.university_id is None:
            raise ValueError('university must be set')
        return super().build()

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering + ['id']
