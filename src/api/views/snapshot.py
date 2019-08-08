from rest_framework.request import Request

from core import models
from api.common import BaseView, ApiResponse
from api.serializers import BaseSnapshotSerializer


class SnapshotListView(BaseView):

    snapshot_model_mapping = {
        'scopus': models.ScopusSnapshot,
        'google-scholar': models.GoogleScholarSnapshot,
        'semantic-scholar': models.SemanticScholarSnapshot,
        'wos': models.WosSnapshot
    }

    def get(self, request: Request, person_id: int):

        snapshots = set(s.strip() for s in request.query_params.get('snapshots', '').split(','))
        snapshots.intersection_update(self.snapshot_model_mapping.keys())
        if not snapshots:
            snapshots = self.snapshot_model_mapping.keys()

        data = {}
        for snapshot in snapshots:
            model = self.snapshot_model_mapping[snapshot]
            qs = model.objects.filter(person_id=person_id)
            serializer = BaseSnapshotSerializer.adjust(model)(qs, many=True)
            data[snapshot] = serializer.data

        return ApiResponse.ok(payload=data)
