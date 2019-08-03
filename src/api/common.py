import platform
from functools import wraps

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class _PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, default=1)
    limit = serializers.IntegerField(min_value=1, required=False)


def parse_pagination(fn):
    @wraps(fn)
    def wrapped(view, request, *args, **kwargs):
        serializer = _PaginationSerializer(data=request.query_params)
        if not serializer.is_valid():
            return ApiResponse.bad_request(
                error_message='Bad pagination',
                validation_errors=serializer.errors
            )
        kwargs.update(serializer.validated_data)
        return fn(view, request, *args, **kwargs)
    return wrapped


def parse_search_term(fn):
    @wraps(fn)
    def wrapped(view, request, *args, **kwargs):
        kwargs['search_term'] = request.query_params.get('t')
        return fn(view, request, *args, **kwargs)
    return wrapped


class _OrderingSerializer(serializers.Serializer):
    o = serializers.RegexField(r'^-?[a-zA-Z_][a-zA-Z_0-9]*(?:,-?[a-zA-Z_][a-zA-Z_0-9]*)*$', required=False)


def parse_ordering(fn):
    @wraps(fn)
    def wrapped(view, request, *args, **kwargs):
        serializer = _OrderingSerializer(data=request.query_params)
        if not serializer.is_valid():
            return ApiResponse.bad_request(
                error_message='Bad ordering',
                validation_errors=serializer.errors
            )
        ordering = serializer.data.get('o')
        if ordering is not None:
            ordering = ordering.split(',')
        kwargs['ordering'] = ordering
        return fn(view, request, *args, **kwargs)
    return wrapped


class BaseView(APIView):
    renderer_classes = (JSONRenderer,)


class ApiResponse(Response):
    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'application/json'
        super().__init__(*args, **kwargs)

    @staticmethod
    def build_data(payload=None, error_message=None, validation_errors=None, error_code=None):
        return {
            'payload': payload,
            'service': {
                'successful': error_message is None and validation_errors is None and error_code is None,
                'error_code': error_code,
                'error_message': error_message,
                'validation_errors': validation_errors or [],
                'node': platform.node()
            }
        }

    @classmethod
    def ok(cls, payload) -> 'ApiResponse':
        return cls(data=cls.build_data(payload=payload), status=status.HTTP_200_OK)

    @classmethod
    def bad_request(cls, error_message=None, validation_errors=None) -> 'ApiResponse':
        return cls(
            data=cls.build_data(error_message=error_message or 'Bad Request', validation_errors=validation_errors),
            status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    def unprocessable_entity(cls, error_message=None) -> 'ApiResponse':
        return cls(
            data=cls.build_data(error_message=error_message or 'Unprocessable Entity'),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @classmethod
    def not_found(cls, error_message=None) -> 'ApiResponse':
        return cls(
            data=cls.build_data(error_message=error_message or 'Not Found'),
            status=status.HTTP_404_NOT_FOUND
        )
