from django.urls import path
from .views import generate_maze_api, solve_maze_api

urlpatterns = [
    path('generate/', generate_maze_api, name='generate_maze'),
    path('solve/', solve_maze_api, name='solve_maze'),
]
