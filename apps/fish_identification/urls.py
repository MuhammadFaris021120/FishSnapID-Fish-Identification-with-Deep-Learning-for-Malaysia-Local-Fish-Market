from django.urls import path
from . import views


urlpatterns = [
    path('identify_fish/', views.identify_fish, name='identify_fish'),
]
