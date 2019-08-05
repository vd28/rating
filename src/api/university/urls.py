from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'(?P<university_id>\d+)/faculties/stats/?', views.FacultyStatsView.as_view())
]
