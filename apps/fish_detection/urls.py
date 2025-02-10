from django.urls import path
from . import views


urlpatterns = [
    path('detect_fish/', views.detect_fish, name='detect_fish'),
]
