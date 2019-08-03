from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'persons/?', views.PersonRatingView.as_view()),
    re_path(r'faculties/?', views.FacultyRatingView.as_view()),
    re_path(r'departments/?', views.DepartmentRatingView.as_view())
]
