from django.urls import path
from . import views

urlpatterns = [
    path('persons/', views.PersonRatingView.as_view()),
    path('faculties/', views.FacultyRatingView.as_view()),
    path('departments/', views.DepartmentRatingView.as_view())
]
