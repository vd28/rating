from django.conf import settings
from django.db import models

from rest_framework.request import Request

from core import queries
from core.pagination import Pagination, Paginator, PageDoesNotExist, FieldDoesNotExist
from api.common import BaseView, ApiResponse
from api.decorators import parse_ordering, parse_search_term, parse_pagination
from api.serializers.article import ArticleSerializer


class ArticlesPaginator(Paginator):
    search_lookups = (
        'article__title__icontains',
    )

    field_lookups = {
        'title': 'article__title'
    }

    def __init__(self, person_id: int):
        super().__init__()
        self.person_id = person_id

    def get_queryset(self) -> models.QuerySet:
        return queries.fetch_articles(self.person_id)


class ArticleListView(BaseView):

    @parse_search_term
    @parse_ordering
    @parse_pagination
    def get(self, request: Request, person_id: int, **kwargs):

        page = kwargs.get('page')
        limit = kwargs.get('limit') or getattr(settings, 'DEFAULT_PER_PAGE', 20)

        paginator = ArticlesPaginator(person_id)
        paginator.set_term(kwargs.get('search_term'))
        paginator.set_ordering(kwargs.get('ordering'))
        paginator.set_pagination(Pagination(page, limit))

        try:
            result = paginator.build()

        except PageDoesNotExist as e:
            return ApiResponse.not_found(error_message=str(e))

        except FieldDoesNotExist as e:
            return ApiResponse.unprocessable_entity(error_message=str(e))

        serializer = ArticleSerializer(result.objects, many=True)

        return ApiResponse.ok(payload={
            'page': result.page,
            'limit': result.limit,
            'total': result.total,
            'articles': serializer.data
        })
