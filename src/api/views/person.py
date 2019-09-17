from rest_framework.request import Request

from core import queries
from api.common import BaseView, ApiResponse
from api.serializers.joint_authors import JointAuthorsSerializer


class JointAuthorListView(BaseView):

    def get(self, request: Request, person_id: int):
        person = queries.fetch_person(person_id)
        joint_authors = queries.fetch_joints_authors(person_id)
        serializer = JointAuthorsSerializer({'self': person, 'joint_authors': joint_authors})
        return ApiResponse.ok(serializer.data)
