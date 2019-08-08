from django.urls import path, re_path, include
from .views import rating, faculty, snapshot

urlpatterns = [
    path('rating/', include([
        re_path('persons/?', rating.PersonRatingView.as_view()),
        re_path('faculties/?', rating.FacultyRatingView.as_view()),
        re_path('departments/?', rating.DepartmentRatingView.as_view())
    ])),
    path('universities/', include([
        re_path('(?P<university_id>[0-9]+)/faculties/stats/?', faculty.FacultyStatsView.as_view())
    ])),
    re_path('persons/(?P<person_id>[0-9]+)/snapshots/?', snapshot.SnapshotListView.as_view())
]
