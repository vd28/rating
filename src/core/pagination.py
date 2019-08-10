from typing import Tuple, Iterable, Any, Optional, List
from django.db import models


class PaginatorError(Exception):
    pass


class FieldDoesNotExist(PaginatorError):
    def __init__(self, field: str):
        super().__init__(f'The field {repr(field)} does not exist.')
        self.field = field


class PageDoesNotExist(PaginatorError):
    def __init__(self, page: int):
        super().__init__(f'The page {page} doest not exist.')
        self.page = page


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


class Paginator:

    field_lookups = {}
    search_lookups = ()
    prefetch_related = ()

    def __init__(self):

        self.ordering = ()
        self.term = None
        self.pagination = None

    def get_queryset(self) -> models.QuerySet:
        raise NotImplementedError

    def set_pagination(self, pagination: Optional[Pagination] = None) -> 'Paginator':
        self.pagination = pagination
        return self

    def set_ordering(self, ordering: Optional[Tuple[str, ...]] = None) -> 'Paginator':
        self.ordering = ordering or ()
        return self

    def set_term(self, term: Optional[str] = None) -> 'Paginator':
        self.term = term
        return self

    def build(self):
        qs = self.get_queryset()
        qs = self.sort(qs)
        qs = self.annotate(qs)
        qs = self.search(qs)

        total = qs.count()

        qs = self.paginate(qs)

        for lookup in self.prefetch_related:
            qs = qs.prefetch_related(lookup)

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

    def annotate(self, qs: models.QuerySet) -> models.QuerySet:
        return qs

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

    @classmethod
    def make_ordering_deterministic(cls, ordering: List[str]) -> List[str]:
        return ordering
