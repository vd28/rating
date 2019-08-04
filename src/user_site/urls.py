from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('rating/persons/', views.PersonRatingView.as_view(), name='person_rating'),
    path('rating/faculties/', views.FacultyRatingView.as_view(), name='faculty_rating'),
    path('rating/departments/', views.DepartmentRatingView.as_view(), name='department_rating'),
    path('config-not-found/', views.ConfigNotFoundView.as_view(), name='config_not_found'),
]