from django.urls import path
from . import views

urlpatterns = [
    path('query_fish_recent_capture/', views.query_fish_recent_capture, name='query_fish_recent_capture'),
    path('query_fish_for_search/', views.query_fish_for_search, name='query_fish_for_search'),
    path('query_fish_collection/', views.query_fish_collection, name='query_fish_collection'),
    path('query_fish_by_local_name/', views.query_fish_by_local_name, name='query_fish_by_local_name'),
    path('create_fish_collection/', views.create_fish_collection, name='create_fish_collection'),
    path('delete_fish_collection/', views.delete_fish_collection, name='delete_fish_collection'),
    path('update_fish_collection/', views.update_fish_collection, name='update_fish_collection'),
    path('create_user_profile/', views.create_user_profile, name='create_user_profile'),
    path('delete_fish_image/', views.delete_fish_image, name='delete_fish_image'),
]
