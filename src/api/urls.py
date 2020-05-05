from django.urls import path, re_path, include
from .views import rating, faculty, snapshot, article, person,knowledge,cooperating

urlpatterns = [
    path('rating/', include([
        re_path('persons/?', rating.PersonRatingView.as_view()),
        re_path('faculties/?', rating.FacultyRatingView.as_view()),
        re_path('departments/?', rating.DepartmentRatingView.as_view())
    ])),

    path('universities/', include([
        re_path('(?P<university_id>[0-9]+)/faculties/stats/?', faculty.FacultyStatsView.as_view())
    ])),

    path('persons/', include([
        re_path('(?P<person_id>[0-9]+)/snapshots/?', snapshot.SnapshotListView.as_view()),
        re_path('(?P<person_id>[0-9]+)/articles/?', article.ArticleListView.as_view()),
        re_path('(?P<person_id>[0-9]+)/joint-authors/?', person.JointAuthorListView.as_view())
    ])),
    path('doc-knowledge/',include([
        re_path('knowledge',knowledge.KnowledgeView.get),
        re_path('cooperating',cooperating.CooperatingViev.get)
    ]))
]
