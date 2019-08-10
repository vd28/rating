from django.db.models import QuerySet
from django.utils import timezone

from rest_framework.request import Request

from core.models import ScopusSnapshot, GoogleScholarSnapshot, SemanticScholarSnapshot, WosSnapshot
from api.common import BaseView, ApiResponse
from api.serializers.snapshot import BaseSnapshotSerializer


def _noop(qs: QuerySet) -> QuerySet:
    return qs


def _year(qs: QuerySet) -> QuerySet:
    return qs.filter(revision__created_at__year=timezone.now().year)


def _quarter(qs: QuerySet) -> QuerySet:
    now = timezone.now()
    return qs.filter(revision__created_at__year=now.year, revision__created_at__quarter=(now.month - 1) // 3 + 1)


def _month(qs: QuerySet) -> QuerySet:
    now = timezone.now()
    return qs.filter(revision__created_at__year=now.year, revision__created_at__month=now.month)


def _week(qs: QuerySet) -> QuerySet:
    year, week, _ = timezone.now().isocalendar()
    return qs.filter(revision__created_at__year=year, revision__created_at__week=week)


class SnapshotListView(BaseView):
    snapshot_model_mapping = {
        'scopus': ScopusSnapshot,
        'google-scholar': GoogleScholarSnapshot,
        'semantic-scholar': SemanticScholarSnapshot,
        'wos': WosSnapshot
    }

    period = {
        '': _noop,
        'year': _year,
        'quarter': _quarter,
        'month': _month,
        'week': _week
    }

    def get(self, request: Request, person_id: int):

        filter_period = self.period.get(request.query_params.get('period', ''))

        snapshots = set(s.strip() for s in request.query_params.get('snapshots', '').split(','))
        snapshots.intersection_update(self.snapshot_model_mapping.keys())
        if not snapshots:
            snapshots = self.snapshot_model_mapping.keys()

        data = {}
        for snapshot in snapshots:
            model = self.snapshot_model_mapping[snapshot]
            qs = filter_period(model.objects.filter(person_id=person_id)).order_by('revision__created_at')
            serializer = BaseSnapshotSerializer.adjust(model)(qs, many=True)
            data[snapshot] = serializer.data

        return ApiResponse.ok(payload=data)
