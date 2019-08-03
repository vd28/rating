from django.urls import path, include

urlpatterns = [
    path('rating/', include('api.rating.urls'))
]
