import platform

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.models import ScopusSnapshot, GoogleScholarSnapshot, SemanticScholarSnapshot, WosSnapshot


SNAPSHOT_MODEL_MAPPING = {
    'scopus': ScopusSnapshot,
    'google-scholar': GoogleScholarSnapshot,
    'semantic-scholar': SemanticScholarSnapshot,
    'wos': WosSnapshot
}


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return False


class BaseView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
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
                'validation_errors': validation_errors,
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
