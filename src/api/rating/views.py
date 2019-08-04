from typing import Dict, Any

from django.conf import settings

from rest_framework.request import Request
from rest_framework.response import Response

from core import models, queries
from core.rating_builder import (
    AbstractRatingBuilder, PersonRatingBuilder, DepartmentRatingBuilder, FacultyRatingBuilder,
    Pagination, PageDoesNotExist, FieldDoesNotExist
)
from api.common import BaseView, ApiResponse, parse_ordering, parse_pagination, parse_search_term
from .serializers import (
    PersonSerializer, DepartmentSerializer, FacultySerializer, BaseRatingOptionsSerializer,
    PersonRatingOptionsSerializer, FacultyRatingOptionsSerializer, DepartmentRatingOptionsSerializer
)


class BaseRatingView(BaseView):

    builder = None
    rating_serializer = None
    options_serializer = BaseRatingOptionsSerializer

    snapshot_model_mapping = {
        BaseRatingOptionsSerializer.SCOPUS: models.ScopusSnapshot,
        BaseRatingOptionsSerializer.GOOGLE_SCHOLAR: models.GoogleScholarSnapshot,
        BaseRatingOptionsSerializer.SEMANTIC_SCHOLAR: models.SemanticScholarSnapshot,
        BaseRatingOptionsSerializer.WOS: models.WosSnapshot
    }

    @parse_search_term
    @parse_ordering
    @parse_pagination
    def post(self, request: Request, *args, **kwargs):

        options_serializer = self.get_options_serializer()(data=request.data)
        if not options_serializer.is_valid():
            return ApiResponse.bad_request(validation_errors=options_serializer.errors)

        page = kwargs.pop('page')
        limit = kwargs.pop('limit', None) or getattr(settings, 'DEFAULT_PER_PAGE', 20)

        revision_id = options_serializer.validated_data.get('revision_id')
        if revision_id is None:
            revision = queries.fetch_latest_revision()
            if revision is None:
                return ApiResponse.ok(payload={
                    'page': page,
                    'limit': limit,
                    'total': 0,
                    'rating': []
                })
            revision_id = revision.id

        revision_type = options_serializer.validated_data.get('revision_type')
        snapshot_model = self.snapshot_model_mapping[revision_type]
        term = kwargs.pop('search_term', None)
        ordering = kwargs.pop('ordering', None)

        builder = self.get_builder()(snapshot_model.get_options())
        builder.set_revision(revision_id)
        builder.set_term(term)
        builder.set_ordering(ordering)
        builder.set_pagination(Pagination(page, limit))

        try:
            result = self.build_rating(request, builder, options_serializer.validated_data)

        except PageDoesNotExist as e:
            return ApiResponse.not_found(error_message=str(e))

        except FieldDoesNotExist as e:
            return ApiResponse.unprocessable_entity(error_message=str(e))

        if isinstance(result, Response):
            return result

        rating_serializer = self.get_rating_serializer().adjust(snapshot_model)(result.objects, many=True)

        return ApiResponse.ok(payload={
            'page': result.page,
            'limit': result.limit,
            'total': result.total,
            'rating': rating_serializer.data
        })

    def build_rating(self, request: Request, builder: AbstractRatingBuilder, options: Dict[str, Any]):
        raise NotImplementedError

    @classmethod
    def get_builder(cls):
        if cls.builder is None:
            raise NotImplementedError("Missing 'builder' class property. "
                                      "You must specify it in child classes.")
        return cls.builder

    @classmethod
    def get_rating_serializer(cls):
        if cls.rating_serializer is None:
            raise NotImplementedError("Missing 'rating_serializer' class property. "
                                      "You must specify it in child classes.")
        return cls.rating_serializer

    @classmethod
    def get_options_serializer(cls):
        return cls.options_serializer


class PersonRatingView(BaseRatingView):

    builder = PersonRatingBuilder
    rating_serializer = PersonSerializer
    options_serializer = PersonRatingOptionsSerializer

    def build_rating(self, request: Request, builder: PersonRatingBuilder, options: Dict[str, Any]):
        builder.set_university(options['university_id'])
        builder.set_person_types(options.get('person_type_ids', ()))
        return builder.build()


class FacultyRatingView(BaseRatingView):

    builder = FacultyRatingBuilder
    rating_serializer = FacultySerializer
    options_serializer = FacultyRatingOptionsSerializer

    def build_rating(self, request: Request, builder: FacultyRatingBuilder, options: Dict[str, Any]):
        builder.set_university(options['university_id'])
        return builder.build()


class DepartmentRatingView(BaseRatingView):

    builder = DepartmentRatingBuilder
    rating_serializer = DepartmentSerializer
    options_serializer = DepartmentRatingOptionsSerializer

    def build_rating(self, request: Request, builder: DepartmentRatingBuilder, options: Dict[str, Any]):
        builder.set_university(options['university_id'])
        return builder.build()
