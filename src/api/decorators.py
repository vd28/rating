from functools import wraps
from rest_framework import serializers
from .common import ApiResponse


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
