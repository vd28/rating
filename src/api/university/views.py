from rest_framework.request import Request

from api.common import BaseView, ApiResponse
from core import queries
from .serializers import FacultySerializer


class FacultyStatsView(BaseView):

    def get(self, request: Request, university_id: int):
        qs = queries.fetch_faculties(university_id, annotate=True).order_by('name', 'id')
        serializer = FacultySerializer(qs, many=True)
        return ApiResponse.ok(payload=serializer.data)
