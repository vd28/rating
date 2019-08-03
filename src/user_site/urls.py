from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('config-not-found/', views.ConfigNotFoundView.as_view(), name='config_not_found'),
]
