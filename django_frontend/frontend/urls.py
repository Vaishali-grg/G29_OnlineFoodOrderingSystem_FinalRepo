from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('readonly/', views.recipe_list_readonly, name='recipe_list_readonly'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('update/<int:recipe_id>/', views.recipe_update, name='recipe_update'),
    path('delete/<int:recipe_id>/', views.recipe_delete, name='recipe_delete'),
]