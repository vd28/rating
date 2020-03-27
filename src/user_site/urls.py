from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('rating/persons/', views.PersonRatingView.as_view(), name='person_rating'),
    path('rating/faculties/', views.FacultyRatingView.as_view(), name='faculty_rating'),
    path('rating/departments/', views.DepartmentRatingView.as_view(), name='department_rating'),
    path('persons/<int:person_id>/', views.PersonView.as_view(), name='person'),
    path('persons/search/', views.PersonsSearchResultsView.as_view(), name='persons_search_results'),
    path('config-not-found/', views.ConfigNotFoundView.as_view(), name='config_not_found'),
    path('department-person/<int:department_id>', views.DepartmentPersonRatingView.as_view(), name='department_person_rating'),
    path('faculty-department/<int:faculty_id>', views.FacultyDepartmentRatingView.as_view(), name='faculty_department_rating'),
    path('doc-knowledge/', views.DocKnowledgeView.as_view(), name='doc_knowledge'),
    path('cooperating/', views.CooperatingView.as_view() ,name='cooperating')
]
